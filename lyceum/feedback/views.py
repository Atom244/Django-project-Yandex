import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms
import feedback.models

__all__ = []


def feedback_views(request):
    template = "feedback/feedback.html"

    files_form = feedback.forms.FilesForm(
        request.POST or None,
        request.FILES or None,
    )

    author_form = feedback.forms.AuthorForm(request.POST or None)

    content_form = feedback.forms.FeedbackForm(request.POST or None)

    if request.method == "POST":
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
                for f in files:
                    multiple_file = (
                        feedback.models.MultipleFile.objects.create(
                            feedback=new_feedback,
                            file=f,
                        )
                    )
                    multiple_file.save()

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
    return django.shortcuts.render(request, template, context)
