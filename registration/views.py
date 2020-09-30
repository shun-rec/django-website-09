from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User


subject = '登録確認'
message_template = """
ご登録ありがとうございます。
以下URLをクリックして登録を完了してください。
https://localhost-shundev-1.paiza-user-free.cloud:8000{}
"""



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # 確認するまでログイン不可にする
        user.is_active = False
        if commit:
            user.save()

            activate_url = reverse_lazy("activate", args=[
                urlsafe_base64_encode(force_bytes(user.pk)),
                default_token_generator.make_token(user),
            ])
            message = message_template.format(activate_url)
            user.email_user(subject, message)
        return user
        

class ActivateView(TemplateView):
    template_name = "registration/activate.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'