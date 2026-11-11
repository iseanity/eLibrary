from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book, UserBookItem
from .forms import RegisterForm

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('profile')
        else:
            return render(request, 'sign_in.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'sign_in.html')

def index_view(request):
    new_books = Book.objects.all()[:4] 
    return render(request, 'index.html', {'new_books': new_books})

def catalog_view(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'catalog.html', {'books': books, 'query': query})

def sign_up_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'sign_up.html', {'form': form})

# Личный кабинет: разделяем книги на два списка
@login_required(login_url='sign_in')
def profile_view(request):
    wish_list = UserBookItem.objects.filter(user=request.user, status='WISH')
    read_list = UserBookItem.objects.filter(user=request.user, status='READ')
    
    is_admin = request.user.is_staff
    all_items = UserBookItem.objects.all() if is_admin else None

    return render(request, 'profile.html', {
        'wish_list': wish_list,
        'read_list': read_list,
        'all_items': all_items,
        'is_admin': is_admin
    })

# CREATE: Добавление книги по умолчанию в статус 'WISH'
@login_required(login_url='sign_in')
def add_to_wishlist_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    UserBookItem.objects.get_or_create(user=request.user, book=book, defaults={'status': 'WISH'})
    return redirect('catalog')

# UPDATE: Быстрое перемещение книги между списками WISH <-> READ
@login_required(login_url='sign_in')
def update_item_status_view(request, item_id):
    item = get_object_or_404(UserBookItem, id=item_id)
    if item.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав на изменение этой записи.")
    
    # Меняем статус на противоположный
    if item.status == 'WISH':
        item.status = 'READ'
    else:
        item.status = 'WISH'
    item.save()
    
    return redirect('profile')

# DELETE: Удаление книги из списка
@login_required(login_url='sign_in')
def delete_item_view(request, item_id):
    item = get_object_or_404(UserBookItem, id=item_id)
    if item.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав на удаление этой записи.")
    item.delete()
    return redirect('profile')