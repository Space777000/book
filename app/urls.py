from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<str:isbn>', views.DetailView.as_view(), name='detail'),
    path('books/<int:page_num>/<keyword>', views.BooksView.as_view(), name='books'),
]