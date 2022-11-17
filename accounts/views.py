from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from .models import Profile

# Create your views here.


def signup(request):
    return render(request, "accounts/signup.html")


def signupNormal(request):
    if request.user.is_authenticated:
        return redirect("main:index")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # 프로필 생성
            auth_login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signupNormal.html", context)


def login(request):
    return render(request, "accounts/login.html")


def loginNormal(request):
    if request.user.is_authenticated:
        return redirect("friends:index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(
                request,
                form.get_user(),
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return redirect(request.GET.get("next") or "friends:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/loginNormal.html", context)


def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 되었습니다.")
    return redirect("main:index")


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    friends = user.friend_set.all()
    print(friends)
    like_friends = user.like_friend.all()

    context = {
        "user": user,
        "friends": friends,
        "like_friends": like_friends,
    }
    return render(request, "accounts/detail.html", context)


@require_POST
@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)

    # 프로필에 해당하는 유저를 로그인한 유저가 팔로우 할 수 없음
    if request.user == user:
        messages.warning(request, "스스로 팔로우 할 수 없습니다.")
        return redirect("accounts:detail", pk)

    # 팔로우 상태면, 팔로우 취소를 누르면 삭제
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        is_followed = False

    # 팔로우 상태가 아니면, '팔로우'를 누르면 추가
    else:
        user.followers.add(request.user)
        is_followed = True

    data = {
        "followers_count": user.followers.count(),
        "followings_count": user.followings.count(),
        "is_followed": is_followed,
    }

    return JsonResponse(data)


# 마이 페이지 (회원 정보로 이동, 비밀번호 변경, 로그아웃, 회원탈퇴)
@login_required
def mypage(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user != user:
        return redirect("main:index")

    context = {
        "user": user,
    }

    return render(request, "accounts/mypage.html", context)


# 비밀번호 변경
@login_required
def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # 로그인 유지
            return redirect("accounts:mypage", request.user.pk)

    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form,
    }

    return render(request, "accounts/password.html", context)


# 회원 탈퇴
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)

    return redirect("main:index")


# 회원 프로필 (프로필 사진, 소개글) (+ 닉네임?)
@login_required
def update(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)

    # 업데이트
    if request.user.profile:
        profile = request.user.profile

        if request.method == "POST":
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            change_form = CustomUserChangeForm(request.POST, instance=user)

            if profile_form.is_valid() and change_form.is_valid():
                profile_form.save()
                change_form.save()
                # return redirect('accounts:detail', request.user.pk)
                return redirect("accounts:mypage", request.user.pk)

        else:
            profile_form = ProfileForm(instance=profile)
            change_form = CustomUserChangeForm(instance=user)

    # 최초 생성
    else:
        if request.method == "POST":
            profile_form = ProfileForm(request.POST, request.FILES)
            change_form = CustomUserChangeForm(request.POST, instance=user)

            if profile_form.is_valid() and change_form.is_valid():
                profile_form.save()
                change_form.save()
                # return redirect('accounts:detail', request.user.pk)
                return redirect("accounts:mypage", request.user.pk)

        else:
            profile_form = ProfileForm()
            change_form = CustomUserChangeForm(instance=user)

    context = {
        "profile_form": profile_form,
        "change_form": change_form,
    }

    return render(request, "accounts/update.html", context)


@login_required
def articles(request, pk):
    articles = all.Articles.objects.filter(user=request.user).order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "accounts/articles.html", context)


import secrets
import requests

state_token = secrets.token_urlsafe(16)

# 네이버 보류
def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "UBnDRMN8PAPnLjvY_ztF"  # 배포시 보안적용 해야함
    redirect_uri = "http://127.0.0.1:8000/accounts/naver/login/callback/"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "UBnDRMN8PAPnLjvY_ztF",  # 배포시 보안적용 해야함
        "client_secret": "34XV68M9Gj",
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://127.0.0.1:8000/accounts/naver/login/callback/",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]
    headers = {"Authorization": f"Bearer ${access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["nickname"]
    naver_email = naver_user_information["response"]["email"]

    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
        auth_login(
            request, naver_user, backend="django.contrib.auth.backends.ModelBackend"
        )
        return redirect(request.GET.get("next") or "friends:index")
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        naver_login_user.email = naver_email
        naver_login_user.set_password(str(state_token))
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
        auth_login(
            request, naver_user, backend="django.contrib.auth.backends.ModelBackend"
        )
        return redirect("friends:index")
