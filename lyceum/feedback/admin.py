from django.contrib import admin

import feedback.models

__all__ = []


class FeedbackInline(admin.StackedInline):
    model = feedback.models.Feedback
    fields = ("text", "status", "created_on")
    readonly_fields = ("text", "created_on")
    can_delete = False
    extra = 0


@admin.register(feedback.models.PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ("name", "mail")
    readonly_fields = ("name", "mail")
    inlines = [FeedbackInline]

    def save_model(self, request, obj, form, change):
        if change and hasattr(obj, "feedbacks"):
            feedback_instance = obj.feedbacks
            new_status = feedback_instance.status
            old_status = feedback.models.Feedback.objects.get(
                pk=feedback_instance.pk,
            ).status

            if new_status != old_status:
                feedback.models.StatusLog.objects.create(
                    user=request.user,
                    feedback=feedback_instance,
                    from_status=old_status,
                    to=new_status,
                )

        super().save_model(request, obj, form, change)

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
