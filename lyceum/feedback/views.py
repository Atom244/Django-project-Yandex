import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.views

import feedback.forms
import feedback.models

__all__ = []


class FeedbackView(django.views.View):
    template_name = "feedback/feedback.html"

    def get(self, request):
        files_form = feedback.forms.FilesForm()
        author_form = feedback.forms.AuthorForm()
        content_form = feedback.forms.FeedbackForm()

        context = {
            "forms": {
                "files_form": files_form,
                "author_form": author_form,
                "content_form": content_form,
            },
        }

        return django.shortcuts.render(request, self.template_name, context)

    def post(self, request):
        files_form = feedback.forms.FilesForm(request.POST, request.FILES)
        author_form = feedback.forms.AuthorForm(request.POST)
        content_form = feedback.forms.FeedbackForm(request.POST)

        if (
            files_form.is_valid()
            and author_form.is_valid()
            and content_form.is_valid()
        ):

            personal_data = author_form.save()

            new_feedback = content_form.save(commit=False)
            new_feedback.personal_data = personal_data
            new_feedback.save()

            files = files_form.cleaned_data["file_field"]

            if files:
                for file in files:
                    feedback.models.MultipleFile.objects.create(
                        feedback=new_feedback,
                        file=file,
                    )

            django.core.mail.send_mail(
                f"FROM: {personal_data.mail}",
                new_feedback.text,
                django.conf.settings.EMAIL_ADDRESS,
                [personal_data.mail],
                fail_silently=False,
            )

            django.contrib.messages.success(
                request=request,
                message="Форма успешно отправлена!",
            )
            return django.shortcuts.redirect("feedback:feedback")

        context = {
            "forms": {
                "files_form": files_form,
                "author_form": author_form,
                "content_form": content_form,
            },
        }
        return django.shortcuts.render(request, self.template_name, context)
