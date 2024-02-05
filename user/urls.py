from django.urls import path
from .views import EmailConfirmationView, CodeVerifyView, SetPasswordView, LogoutVerifyView, \
    LogoutView, LoginView, EditProfileView, ChangePassView, resend_code, ForgotPassword

app_name = 'user'

urlpatterns = [
    path('email-confirm/', EmailConfirmationView.as_view(), name='email_confirm'),
    path('code-verify/', CodeVerifyView.as_view(), name='code_verify'),
    path('set-password/', SetPasswordView.as_view(), name='set_password'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout-verify/', LogoutVerifyView.as_view(), name='logout_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change-password/', ChangePassView.as_view(), name='change_pass'),
    path('resend-code/', resend_code, name='resend_code'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_pass'),

]