from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from main import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Banner, Service, AboutUs, Price,

def index(request):
    contacts = models.Contact.objects.filter(is_show=False).count()
    context = {
        'contacts':contacts
    }
    return render(request, 'dashboard/index.html', context)

# @login_required(login_url='dashboard:log_in')
# def create_banner(request):
#     if request.method == "POST":
#             title = request.POST['title']
#             body = request.POST['body']
#             models.Banner.objects.create(
#             title=title,
#             body=body,
#         )
        
#     return render(request, 'dashboard/banner/create.html')

@login_required(login_url='dashboard:log_in')
def create_banner(request):
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        try:
            models.Banner.objects.create(title=title, body=body)
            messages.success(request, 'Banner yaratildi!')
        except Exception as e:
            messages.error(request, f'Banner yaratishda xatolik yuz berdi: {e}')
        
    return render(request, 'dashboard/banner/create.html')

@login_required(login_url='dashboard:log_in')
def list_banner(request):
    banners = models.Banner.objects.all()
    context = {
        'banners':banners
    }
    return render(request, 'dashboard/banner/list.html', context)

@login_required(login_url='dashboard:log_in')
def banner_detail(request, id):
    banner = models.Banner.objects.get(id=id)
    context = {
        'banner':banner
    }
    return render(request, 'dashboard/banner/detail.html', context)

# @login_required(login_url='dashboard:log_in')
# def banner_edit(request, id):
#     banner = models.Banner.objects.get(id=id)
#     if request.method == 'POST':
#         banner.title = request.POST['title']
#         banner.body = request.POST['body']
#         banner.save()
#         return redirect('banner_detail', banner.id)
#     context = {
#         'banner':banner
#     }
#     return render(request, 'dashboard/banner/edit.html', context)
@login_required(login_url='dashboard:log_in')
def banner_edit(request, id):
    banner = models.Banner.objects.get(id=id)
    if request.method == 'POST':
        banner.title = request.POST['title']
        banner.body = request.POST['body']
        try:
            banner.save()
            messages.success(request, "Banner muvaffaqiyatli o'zgartirildi!")
            return redirect('banner_detail', banner.id)
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {e}")
    context = {
        'banner': banner
    }
    return render(request, 'dashboard/banner/edit.html', context)

# @login_required(login_url='dashboard:log_in')
# def banner_delete(request, id):
#     models.Banner.objects.get(id=id).delete()
#     return redirect('list_banner')
@login_required(login_url='dashboard:log_in')
def banner_delete(request, id):
    try:
        banner = models.Banner.objects.get(id=id)
        banner.delete()
        messages.success(request, "Banner muvaffaqiyatli o'chirildi!")
    except models.Banner.DoesNotExist:
        messages.error(request, "Bunday IDga ega banner topilmadi.")
    except Exception as e:
        messages.error(request, f"O'chirishda xatolik yuz berdi: {e}")


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         password_confirm = request.POST['password_confirm']
#         if password == password_confirm:
#             User.objects.create_user(
#                 username = username,
#                 password = password
#             )
#     return render(request, 'dashboard/auth/register.html')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password == password_confirm:
            try:
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!")
                return redirect('dashboard/index.html')
            except Exception as e:
                messages.error(request, f"Ro'yxatdan o'tishda xatolik yuz berdi: {e}")
        else:
            messages.error(request, 'Parollar mos kelmadi.')
            
    return render(request, 'dashboard/auth/register.html')



# def log_in(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(
#             username = username, 
#             password = password
#             )
#         if user:
#             login(request, user)
#             return redirect('dashboard:index')
#         else:
#             ...

#     return render(request, 'dashboard/auth/login.html')
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Siz muvaffaqiyatli tizimga kirdingiz!')
            return redirect('dashboard/auth/register.html')
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")
            
    return render(request, 'dashboard/auth/login.html')

# @login_required(login_url='dashboard:log_in')
# def log_out(request):
#     logout(request)
#     return redirect('main:index')
def log_out(request):
    logout(request)
    messages.info(request, 'Siz muvaffaqiyatli tizmdan chiqdingiz.')
    return redirect('main:index')


def search(request):
    query = request.GET.get('q', '')
    if query:
        results = {
            'banners': Banner.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)),
            'services': Service.objects.filter(Q(name__icontains=query) | Q(body__icontains=query)),
            'about_us': AboutUs.objects.filter(body__icontains=query),
            'prices': Price.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)),
        }
    else:
        results = {}
    return render(request, 'search_results.html', {'results': results})