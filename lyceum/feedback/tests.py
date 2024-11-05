from pathlib import Path
import shutil

import django.conf
from django.core.files.uploadedfile import SimpleUploadedFile
import django.test
import django.urls
import parameterized

import feedback.forms
import feedback.models


__all__ = []


class FeedbackTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()
        cls.media_root = Path("media_test")
        django.conf.settings.MEDIA_ROOT = cls.media_root
        cls.media_root.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if cls.media_root.exists():
            shutil.rmtree(cls.media_root)

    def test_feedback_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertIsInstance(form, feedback.forms.FeedbackForm)

    @parameterized.parameterized.expand(
        [
            ("text", "Текст отзыва"),
            ("mail", "Почта"),
            ("name", "Имя"),
        ],
    )
    def test_feedback_labels(self, field, expected_text):
        label = self.form.fields[field].label
        self.assertEqual(label, expected_text)

    @parameterized.parameterized.expand(
        [
            ("text", "Оставьте отзыв"),
            ("mail", "Ваш электронный адрес"),
            ("name", "Имя автора письма"),
        ],
    )
    def test_feedback_help_texts(self, field, expected_text):
        help_text = self.form.fields[field].help_text
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

    def test_correct_data_form_submit(self):
        form_data = {
            "text": "Good text",
            "mail": "good@mail.ru",
            "name": "Test Name",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertTrue(form.is_valid())

    def test_incorrect_data_form_submit(self):
        form_data = {
            "text": "Bad text",
            "mail": "a@a.a",
            "name": "bad name",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Некорректный e-mail адрес", form.errors["mail"])

    def test_empty_fields(self):
        form_data = {
            "text": "",
            "mail": "",
            "name": "",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("mail"))
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

        self.assertEqual(response.status_code, 200)

        feedback_instance = feedback.models.Feedback.objects.last()

        upload_path = (
            Path(django.conf.settings.MEDIA_ROOT)
            / f"uploads/{feedback_instance.id}/"
        )
        self.assertTrue(upload_path.is_dir())
        self.assertTrue((upload_path / "test_file.txt").is_file())
