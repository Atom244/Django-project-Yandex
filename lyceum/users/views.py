from datetime import timedelta

import django.conf
from django.contrib import messages
import django.contrib.auth
import django.contrib.auth.decorators
from django.contrib.auth.models import User
import django.core.mail
import django.http
import django.shortcuts
from django.shortcuts import get_object_or_404, redirect
import django.urls
from django.utils import timezone

import users.forms
import users.models


__all__ = []


def signup(request):
    template = "users/signup.html"
    form = users.forms.SignUpForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            users.models.Profile.objects.create(
                user=user,
            )

            if django.conf.settings.DEFAULT_USER_IS_ACTIVE:
                user.is_active = True
                user.save()

            activation_link = request.build_absolute_uri(
                django.urls.reverse(
                    "users:activate",
                    kwargs={
                        "username": user.username,
                    },
                ),
            )

            msg_text = (
                f"Вам необходимо активировать аккаунт в течение 12 "
                "часов после регистрации. "
                "Для активации перейдите по ссылке, указанной в"
                " данном письме.\n"
                f"Ссылка для активации: {activation_link}"
            )

            django.core.mail.send_mail(
                "Активация аккаунта",
                msg_text,
                django.conf.settings.EMAIL_ADDRESS,
                [user.email],
            )

            django.contrib.auth.login(
                request,
                user,
                backend="users.backends.LoginBackend",
            )
            return django.shortcuts.redirect(
                django.urls.reverse("homepage:home"),
            )

    return django.shortcuts.render(request, template, context)


def activate_user(request, username):
    user = User.objects.get(
        username=username,
    )
    if timezone.now() - timedelta(hours=12) <= user.date_joined:
        user.is_active = True
        user.save()
        return django.shortcuts.redirect("users:login")

    return django.http.HttpResponseNotFound(
        "Пользователь не найден или время активации истекло",
    )


def reactivate_user(request, username):
    profile = get_object_or_404(users.models.Profile, user__username=username)

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


def user_list(request):
    template = "users/user_list.html"
    active_users = users.models.ProxyUser.objects.active().all()
    context = {
        "users": active_users,
    }
    return django.shortcuts.render(request, template, context)


def user_detail(request, pk):
    template = "users/user_detail.html"
    user = django.shortcuts.get_object_or_404(
        users.models.ProxyUser.objects.get_user_detail(pk),
    )
    context = {
        "user": user,
    }
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    user = request.user

    user_form = users.forms.UserEditForm(
        request.POST or None,
        initial={
            "first_name": user.first_name if user.first_name else "",
            "last_name": user.last_name if user.last_name else "",
            "username": user.username,
            "email": user.email,
        },
        instance=user,
    )

    birthday = user.profile.birthday
    if user.profile.birthday:
        user.profile.birthday.isoformat()

    profile_form = users.forms.ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        initial={
            "image": user.profile.image,
            "birthday": birthday,
        },
        instance=user.profile,
    )

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return django.shortcuts.redirect("users:profile")

    if not user.is_authenticated:
        return django.shortcuts.redirect("users:login")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "coffee_count": user.profile.coffee_count,
    }
    return django.shortcuts.render(request, template, context)
