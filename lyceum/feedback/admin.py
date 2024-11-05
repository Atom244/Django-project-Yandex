from django.contrib import admin

import feedback.models

__all__ = []


class FeedbackInline(admin.StackedInline):
    model = feedback.models.Feedback
    fields = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
    )
    readonly_fields = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.created_on.field.name,
    )
    can_delete = False
    extra = 0


@admin.register(feedback.models.PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = (feedback.models.PersonalData.name.field.name,)
    list_display_links = (feedback.models.PersonalData.name.field.name,)
    readonly_fields = (
        feedback.models.PersonalData.name.field.name,
        feedback.models.PersonalData.mail.field.name,
    )
    inlines = [FeedbackInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        feedback_instance = form.instance.feedbacks
        for formset in formsets:
            for feedback_form in formset:
                if (
                    "status" in feedback_form.cleaned_data
                    and feedback_form.cleaned_data["status"]
                    != feedback_form.initial.get("status")
                ):
                    feedback.models.StatusLog.objects.create(
                        user=request.user,
                        from_status=feedback_form.initial.get("status"),
                        to=feedback_form.cleaned_data["status"],
                        feedback=feedback_instance,
                    )

    def has_delete_permission(self, request, obj=None):
        if obj and hasattr(obj, "feedbacks"):
            return False

        return super().has_delete_permission(request, obj)


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
    )
    readonly_fields = (
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
    )
