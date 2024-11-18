from datetime import timedelta

import django.conf
from django.contrib import messages
import django.contrib.auth
import django.contrib.auth.decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import django.core.mail
import django.http
import django.shortcuts
from django.shortcuts import get_object_or_404, redirect
import django.urls
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, View

import users.forms
import users.models


__all__ = []


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = users.forms.SignUpForm

    def form_valid(self, form):
        user = form.save()

        users.models.Profile.objects.create(user=user)

        if django.conf.settings.DEFAULT_USER_IS_ACTIVE:
            user.is_active = True
            user.save()

        activation_link = self.request.build_absolute_uri(
            django.urls.reverse(
                "users:activate",
                kwargs={"username": user.username},
            ),
        )

        msg_text = (
            f"Вам необходимо активировать аккаунт в течение 12 часов после "
            "регистрации. "
            f"Для активации перейдите по ссылке, указанной в данном письме.\n"
            f"Ссылка для активации: {activation_link}"
        )

        django.core.mail.send_mail(
            "Активация аккаунта",
            msg_text,
            django.conf.settings.EMAIL_ADDRESS,
            [user.email],
        )

        django.contrib.auth.login(
            self.request,
            user,
            backend="users.backends.LoginBackend",
        )

        return redirect(django.urls.reverse("homepage:home"))

    def form_invalid(self, form):
        return super().form_invalid(form)


class ActivateUserView(View):
    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return django.http.HttpResponseNotFound(
                "Пользователь не найден или время активации истекло",
            )

        if timezone.now() - timedelta(hours=12) <= user.date_joined:
            user.is_active = True
            user.save()
            return redirect("users:login")

        return django.http.HttpResponseNotFound(
            "Пользователь не найден или время активации истекло",
        )


class ReactivateUserView(View):
    def get(self, request, username, *args, **kwargs):
        profile = get_object_or_404(
            users.models.Profile,
            user__username=username,
        )

        if (
            profile.activation_sent_at
            and timezone.now() - profile.activation_sent_at > timedelta(days=7)
        ):
            messages.error(
                request,
                "Ссылка для активации больше не действительна. Обратитесь в "
                "поддержку.",
            )
            return redirect("users:login")

        profile.user.is_active = True
        profile.user.save()
        messages.success(request, "Ваш аккаунт успешно активирован.")
        return redirect("users:login")


class UserList(ListView):
    queryset = users.models.ProxyUser.objects.active().all()
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetail(DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return users.models.ProxyUser.objects.get_user_detail(pk)


class Profile(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = kwargs
        context["coffee_count"] = self.request.user.profile.coffee_count
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        user_form = users.forms.UserEditForm(
            initial={
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "username": user.username,
                "email": user.email,
            },
            instance=user,
        )

        birthday = (
            user.profile.birthday.isoformat()
            if user.profile.birthday
            else None
        )

        profile_form = users.forms.ProfileEditForm(
            initial={
                "image": user.profile.image,
                "birthday": birthday,
            },
            instance=user.profile,
        )

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form,
            coffee_count=user.profile.coffee_count,
        )
        return django.shortcuts.render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user

        user_form = users.forms.UserEditForm(
            request.POST,
            instance=user,
        )
        profile_form = users.forms.ProfileEditForm(
            request.POST,
            request.FILES,
            instance=user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user
            profile_instance.save()

            return redirect(django.urls.reverse("users:profile"))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form,
            coffee_count=user.profile.coffee_count,
        )
        return self.re(context)
