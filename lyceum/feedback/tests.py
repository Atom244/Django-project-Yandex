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
