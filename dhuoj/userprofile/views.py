from .forms import UserLoginForm, UserRegisterForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from .forms import ProfileForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(
                username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("home:home")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("home:home")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("home:home")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def profile(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404("用户不存在!")

    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        raise Http404("个人信息不存在!")

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, 'userprofile/profile.html', context)


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段

    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            profile.email = profile_cd['email']
            profile.major = profile_cd['major']
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form,
                   'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
