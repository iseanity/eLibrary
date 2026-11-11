from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.CharField(max_length=200, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5, verbose_name="Рейтинг")
    cover = models.CharField(max_length=255, verbose_name="Путь к обложке")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title

class UserBookItem(models.Model):
    STATUS_CHOICES = [
        ('WISH', 'Хочу прочитать'),
        ('READ', 'Прочитано'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WISH', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"