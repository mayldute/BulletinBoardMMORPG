from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from allauth.account.views import SignupView
from allauth.account.models import EmailAddress
from .models import EmailVerificationCode
from .forms import VerificationCodeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from announcement.models import Announcement, Respond
from .filters import UserAnnouncementFilter, UserRespondFilter, IncomingRespondFilter


class CustomSignupView(SignupView):
    def form_valid(self, form):
        user = form.save(self.request)

        user.is_active = False
        user.save()

        code_instance, created = EmailVerificationCode.objects.get_or_create(user=user)

        if created:
            send_mail(
                'Ваш код подтверждения',
                f'Ваш код подтверждения: {code_instance.code}',
                'no-reply@myproject.com',
                [user.email],
                fail_silently=False,
            )

        messages.info(self.request, "Пожалуйста, введите код подтверждения, который был отправлен на вашу почту.")
        return redirect('verify_email')

def verify_email(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                verification_instance = EmailVerificationCode.objects.get(code=code)
                
                if verification_instance.is_expired():
                    messages.error(request, "Код истек, запросите новый.")
                    return redirect('resend_code')  

                user = verification_instance.user
                user.is_active = True  
                user.save()

                email_address, created = EmailAddress.objects.get_or_create(user=user, email=user.email)
                email_address.verified = True
                email_address.primary = True
                email_address.save()

                verification_instance.delete()

                login(request, user)
                messages.success(request, "Ваш email подтвержден!")
                return redirect('/announcement/')  
                
            except EmailVerificationCode.DoesNotExist:
                messages.error(request, "Неверный код.")
    else:
        form = VerificationCodeForm()

    return render(request, 'users/verify_email.html', {'form': form})


def resend_code(request):
    user = request.user
    EmailVerificationCode.objects.filter(user=user).delete()  
    new_code = EmailVerificationCode.objects.create(user=user)

    send_mail(
        'Ваш новый код подтверждения',
        f'Ваш новый код: {new_code.code}',
        'no-reply@myproject.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, "Новый код отправлен на вашу почту.")
    return redirect('verify_email')

class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Получаем текущего пользователя

        # Фильтрация объявлений пользователя
        user_announcements = Announcement.objects.filter(user=user)
        context['user_announcements'] = UserAnnouncementFilter(self.request.GET, queryset=user_announcements).qs

        # Фильтрация откликов, оставленных пользователем
        user_responds = Respond.objects.filter(user=user)
        context['user_responds'] = UserRespondFilter(self.request.GET, queryset=user_responds).qs

        # Фильтрация входящих откликов (на объявления текущего пользователя)
        incoming_responses = Respond.objects.filter(announcement__user=user)
        context['incoming_responses'] = IncomingRespondFilter(
            self.request.GET,
            queryset=incoming_responses,
            user=user  # Передаем пользователя в фильтр
        ).qs

        # Добавляем фильтры в контекст для использования в шаблоне
        context['user_announcement_filter'] = UserAnnouncementFilter(self.request.GET, queryset=user_announcements)
        context['user_respond_filter'] = UserRespondFilter(self.request.GET, queryset=user_responds)
        context['incoming_respond_filter'] = IncomingRespondFilter(
            self.request.GET,
            queryset=incoming_responses,
            user=user
        )

        return context
    
    
   