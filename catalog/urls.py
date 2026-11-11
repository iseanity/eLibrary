from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index_view, name='index'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('sign-up/', views.sign_up_view, name='sign_up'),
    path('sign-in/', views.sign_in_view, name='sign_in'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # CRUD маршруты для работы со списком книг пользователя
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('item/update/<int:item_id>/', views.update_item_status_view, name='update_item_status'),
    path('item/delete/<int:item_id>/', views.delete_item_view, name='delete_item'),
]