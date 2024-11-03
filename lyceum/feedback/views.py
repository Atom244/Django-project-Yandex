import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms
import feedback.models


__all__ = []


def feedback_views(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_feedback = feedback.models.Feedback(**form.cleaned_data)
            new_feedback.save()

            django.core.mail.send_mail(
                f"FROM: {new_feedback.mail}",
                new_feedback.text,
                django.conf.settings.EMAIL_ADDRESS,
                [new_feedback.mail],
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
