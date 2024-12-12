
def home(request):
    return render(request, 'home.html')
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User  

def index(request):
    return render(request, 'index.html')



def verify_code(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        verification_code = request.POST.get('verification_code')

        user = User.objects.filter(phone_number=phone_number).first()

        if user:
            if user.verification_code == verification_code and user.code_expiration > timezone.now():
                user.is_verified = True
                user.save()
                return redirect('home')  
            else:
                return HttpResponse("Kod noto'g'ri yoki kod muddati o'tgan.")
        else:
            return HttpResponse("Foydalanuvchi topilmadi.")
    return redirect('index')  


def home(request):
    return render(request, 'home.html')
