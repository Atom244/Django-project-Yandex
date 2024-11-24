import http
from pathlib import Path

import django.conf
from django.core.files.uploadedfile import SimpleUploadedFile
import django.test
from django.test import override_settings
import django.urls
import parameterized

import feedback.forms
import feedback.models


__all__ = []


@override_settings(MEDIA_ROOT=Path("media_test"))
class FeedbackTests(django.test.TestCase):
    def test_feedback_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        form = response.context["forms"]
        self.assertIsInstance(
            form["content_form"],
            feedback.forms.FeedbackForm,
        )
        self.assertIsInstance(form["author_form"], feedback.forms.AuthorForm)
        self.assertIsInstance(form["files_form"], feedback.forms.FilesForm)

    @parameterized.parameterized.expand(
        [
            ("content_form", "text", "Текст отзыва"),
            ("author_form", "mail", "Почта"),
            ("author_form", "name", "Имя"),
        ],
    )
    def test_feedback_labels(self, form_name, field, expected_text):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        forms = response.context["forms"]
        form = forms[form_name]
        label = form.fields[field].label
        self.assertEqual(label, expected_text)

    @parameterized.parameterized.expand(
        [
            ("content_form", "text", "Оставьте отзыв"),
            ("author_form", "mail", "Ваш электронный адрес"),
            ("author_form", "name", "Имя автора письма"),
        ],
    )
    def test_feedback_help_texts(self, form_name, field, expected_text):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        forms = response.context["forms"]
        form = forms[form_name]
        help_text = form.fields[field].help_text
        self.assertEqual(help_text, expected_text)

    def test_feedback_redirect_after_submit(self):
        form_data = {
            "text": "Test text for feedback",
            "mail": "1@examplemail.com",
            "name": "Test Name",
        }
        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )

    def test_correct_data_author_form_submit(self):
        form_data = {
            "mail": "good@mail.ru",
            "name": "Test Name",
        }
        form = feedback.forms.AuthorForm(form_data)
        self.assertTrue(form.is_valid())

    def test_correct_data_content_form_submit(self):
        form_data = {
            "text": "Good text",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertTrue(form.is_valid())

    def test_incorrect_data_author_form_submit(self):
        form_data = {
            "mail": "a@a.a",
            "name": "bad name",
        }
        form = feedback.forms.AuthorForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Некорректный e-mail адрес", form.errors["mail"])

    def test_empty_fields_author_form(self):
        form_data = {
            "mail": "",
            "name": "",
        }
        form = feedback.forms.AuthorForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("mail"))

    def test_empty_fields_content_form(self):
        form_data = {
            "text": "",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("text"))

    def test_save_correct_feedback_form_in_model(self):
        form_data = {
            "text": "some text",
            "mail": "test@mail.com",
            "name": "Some Name",
        }
        count = feedback.models.Feedback.objects.count()
        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            count + 1,
        )

    def test_save_incorrect_feedback_form_in_model(self):
        form_data = {
            "text": "some text",
            "mail": "l@mY.p",
            "name": "Some Name",
        }
        count = feedback.models.Feedback.objects.count()
        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            count,
        )

    def test_file_upload(self):
        test_file = SimpleUploadedFile(
            "test_file.txt",
            b"Test file content",
            content_type="text/plain",
        )

        response = self.client.post(
            django.urls.reverse("feedback:feedback"),
            {
                "name": "Test User",
                "text": "This is a test feedback.",
                "mail": "test@example.com",
                "file_field": [test_file],
            },
            follow=True,
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        feedback_instance = feedback.models.Feedback.objects.last()

        upload_path = (
            Path(django.conf.settings.MEDIA_ROOT)
            / f"uploads/{feedback_instance.id}/"
        )
        self.assertTrue(upload_path.is_dir())
        self.assertTrue((upload_path / "test_file.txt").is_file())
