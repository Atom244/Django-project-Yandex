import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms
import feedback.models

__all__ = []


def feedback_views(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(
        request.POST or None,
        request.FILES or None,
    )

    files_form = feedback.forms.FeedbackForm(
        request.POST or None,
        request.FILES or None,
    )
    files_form.fields = {key: files_form.fields[key] for key in ["file_field"]}

    author_form = feedback.forms.FeedbackForm(request.POST or None)
    author_form.fields = {
        key: author_form.fields[key] for key in ["name", "mail"]
    }

    content_form = feedback.forms.FeedbackForm(request.POST or None)
    content_form.fields = {key: content_form.fields[key] for key in ["text"]}

    if request.method == "POST":
        if form.is_valid():
            personal_data = feedback.models.PersonalData(
                name=form.cleaned_data["name"],
                mail=form.cleaned_data["mail"],
            )
            personal_data.save()

            new_feedback = feedback.models.Feedback(
                personal_data=personal_data,
                text=form.cleaned_data["text"],
            )
            new_feedback.save()

            files = form.cleaned_data["file_field"]
            if files:
                for f in files:
                    multiple_file = feedback.models.MultipleFile(
                        feedback=new_feedback,
                        file=f,
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
        "form": form,
        "files_form": files_form,
        "author_form": author_form,
        "content_form": content_form,
    }
    return django.shortcuts.render(request, template, context)
