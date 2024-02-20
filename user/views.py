from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View

from .forms import EmailConfirmationForm, CodeVerifyForm, SetPasswordForm, LoginForm, EditProfileForm, ChangePassForm, \
    ForgotPasswordForm
from .models import User, UserConfirmation
from news.task import send_email


class EmailConfirmationView(View):
    def get(self, request):
        form = EmailConfirmationForm
        context = {
            'form': form,
        }
        return render(request, 'user/email-confirmation.html', context)

    def post(self, request):
        form = EmailConfirmationForm(data=request.POST)

        if form.is_valid():
            cleaned_email = form.cleaned_data.get('email').lower()
            obj = User.objects.filter(email=cleaned_email, registration_complete=True).first()
            if not obj:
                form.save()
                user = User.objects.filter(email=cleaned_email).first()
                code = user.create_verify_code()
                print(code)
                login(request, user)
                # send_email.delay('検証コード', f"あなたの検証コードは {code} です", [cleaned_email])
                send_email('検証コード', f"あなたの検証コードは {code} です", [cleaned_email])
                return redirect('user:code_verify')
            else:
                messages.error(request, "Registration is on process. Check your mail for confirmation code or press the resend button")
                return redirect('user:code_verify')
        else:
            form = EmailConfirmationForm()
            context = {'form': form}
            messages.error(request, "Enter the valid email adress")
            return render(request, 'user/email-confirmation.html', context)


class ForgotPassword(View):
    def get(self, request):
        form = ForgotPasswordForm
        context = {
            'form': form,
        }
        return render(request, 'user/pass_forgot.html', context)

    def post(self, request):
        form = ForgotPasswordForm(data=request.POST)

        if form.is_valid():
            cleaned_email = form.cleaned_data.get('email').lower()
            obj = User.objects.filter(email=cleaned_email, registration_complete=True).first()

            if obj:
                code = obj.create_verify_code()
                send_email('検証コード', f"あなたの検証コードは {code} です", [obj.email])
                login(request, obj)
                return redirect('user:code_verify')
            else:
                form.add_error('email', 'User with this email does not exist or is not registered.')
                context = {'form': form}
                return render(request, 'user/email-confirmation.html', context)
        else:
            context = {'form': form}
            return render(request, 'user/email-confirmation.html', context)


class CodeVerifyView(View):
    def get(self, request):
        form = CodeVerifyForm()
        context = {
            'form': form
        }

        return render(request, 'user/code-verify.html', context)

    def post(self, request):
        form = CodeVerifyForm(data=request.POST)
        user = request.user
        if form.is_valid():
            code = form.cleaned_data.get('code')
            obj = UserConfirmation.objects.filter(user=user, code=code,
                                                  expiration_time__gte=datetime.now(),
                                                  is_confirmed=False
            )
            if obj.exists():
                obj.is_confirmed = True
                return redirect('user:set_password')
            else:
                return redirect('main:error')
        else:
            form = CodeVerifyForm()
            context = {
                'form': form
            }
            return render(request, 'user/code-verify.html', context)


def resend_code(request):
    user = request.user
    if not user.registration_complete:
        confirmation = UserConfirmation.objects.filter(user=user, expiration_time__gte=datetime.now()).first()
        if confirmation:
            messages.error(request, f"You can resend code in {confirmation.expiration_time}")
            return redirect('user:code_verify')
        else:
            code = user.create_verify_code()
            email = user.email
            print(code)
            # send_email.delay('検証コード', f"あなたの検証コードは {code} です", [cleaned_email])
            send_email('認証コード', f"あなたの認証コードは {code} です", [email])
            messages.success(request, "We sent you confirmation code again. Please check your mailbox")
            return redirect('user:code_verify')
    else:
        messages.error(request, "Your profile is complete already")
        return redirect('user:login')


class SetPasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = SetPasswordForm()
        context = {
            'form': form
        }
        return render(request, 'user/set-password.html', context)

    def post(self, request):
        form = SetPasswordForm(data=request.POST)
        user = request.user

        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')
            try:
                if not validate_password(password):
                    if password == password_confirm:
                        user.password = password
                        user.registration_complete = True
                        user.save()
                        login(request, user)
                        return redirect('news_app:home')
                    else:
                        return redirect('main:error')
            except ValidationError:
                return redirect('main:error')
        else:
            form = SetPasswordForm()
            context = {
                'form': form
            }
            return render(request, 'user/set-password.html', context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'user/login.html', context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password')

            user = User.objects.filter(email=email).first()

            if user:
                if user.own_check_password(password):
                    login(request, user)
                    return redirect('news_app:home')
                else:
                    return redirect('main:error')
            else:
                return redirect('main:error')
        else:
            form = LoginForm()
            context = {
                'form': form
            }
            return render(request, 'user/login.html', context)


class LogoutVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/logout-verify.html')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully logged out')
        return redirect('user:login')


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'user/edit-profile.html', context)

    def post(self, request):
        form = EditProfileForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('news_app:history_saved')
        else:
            return redirect('main:error')


class ChangePassView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePassForm()

        context = {
            'form': form
        }
        return render(request, 'user/change-pass.html', context)

    def post(self, request):
        form = ChangePassForm(data=request.POST)
        user = request.user

        if form.is_valid():
            password = form.cleaned_data.get('password')
            if user.check_password(password):
                return redirect('user:set_password')
            else:
                return redirect('main:error')
        else:
            return redirect('main:error')














