
import random

from .models import CustomUser,Emailcode
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
def send_otp(user):
    code=str(random.randint(100000,999999))
    Emailcode.objects.update_or_create(user=user,defaults={'code':code,'created_at':timezone.now()})
    try:
        send_mail(
            'Tasdiqlash kodi',
            f"Sizning ro'yxatdan o'tish kodingiz: {code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"❌ Email yuborishda xatolik: {e}")
        return False


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser


class RegisterView(View):

    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        if password != password2:
            messages.error(request, "Parollar mos emas")
            return redirect('register')


        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username band")
            return redirect('register')


        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro‘yxatdan o‘tgan")
            return redirect('register')


        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Muvaffaqiyatli ro‘yxatdan o‘tdingiz")
        return redirect('login')


class VerifyEmailView(View):
    def get(self, request):
        return render(request, 'auth/verify_otp.html')

    def post(self, request):
        code = request.POST.get('code')
        user_id = request.session.get('temp_user_id')

        if not user_id:
            return redirect('register')

        try:
            email_obj = Emailcode.objects.get(users_id=user_id, code=code)
            if email_obj.is_valid():
                user = email_obj.users
                user.is_active = True
                user.save()
                email_obj.delete()
                return redirect('login')
            else:
                return render(request, 'auth/verify_otp.html', {'error': 'Kod vaqti o‘tgan!'})
        except Emailcode.DoesNotExist:
            return render(request, 'auth/verify_otp.html', {'error': 'Noto‘g‘ri kod!'})


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'error': 'Username yoki parol xato!'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ResendOTPView(View):
    def get(self, request):
        user_id = request.session.get('temp_user_id')
        if not user_id:
            return redirect('register')

        try:
            user = CustomUser.objects.get(id=user_id)
            if send_otp(user):
                return redirect('verify_otp')
            else:
                user.delete()
                return render(request, 'auth/verify_otp.html', {'error': 'Email yuborishda xato!'})
        except CustomUser.DoesNotExist:
            return redirect('register')





