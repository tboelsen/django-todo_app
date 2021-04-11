from django.urls import path
from .views import RegisterView, UserLoginView, TodoListView, TodoCreateView, TodoUpdateView, TodoDeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', TodoListView.as_view(), name='home'),
    path('todo/create/', TodoCreateView.as_view(), name='create'),
    path('todo/update/<int:pk>/', TodoUpdateView.as_view(), name='update'),
    path('todo/delete/<int:pk>/', TodoDeleteView.as_view(), name='delete'),
]
