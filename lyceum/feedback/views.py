from pathlib import Path

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

    if request.method == "POST":
        if form.is_valid():
            personal_data, created = (
                feedback.models.PersonalData.objects.get_or_create(
                    name=form.cleaned_data["name"],
                    mail=form.cleaned_data["mail"],
                )
            )

            new_feedback = feedback.models.Feedback(
                personal_data=personal_data,
                text=form.cleaned_data["text"],
            )
            new_feedback.save()

            files = form.cleaned_data["file_field"]
            if files:
                feedback_id = new_feedback.id
                upload_path = (
                    Path(django.conf.settings.MEDIA_ROOT)
                    / f"uploads/{feedback_id}/"
                )
                upload_path.mkdir(parents=True, exist_ok=True)

                for f in files:
                    multiple_file = feedback.models.MultipleFile(
                        feedback=new_feedback,
                        file=f,
                    )
                    multiple_file.save()
                    file_path = upload_path / f.name
                    with file_path.open("wb+") as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)

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
    }
    return django.shortcuts.render(request, template, context)
