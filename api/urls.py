from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/',views.TaskView.as_view(),name='tasks'),
    path('taskDetail/<int:pk>/',views.TaskDetailView.as_view(),name='taskDetail'),
    path('register/',views.RegisterationView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('refresh/token/',TokenRefreshView.as_view()),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('forget/',views.ForgetView.as_view(),name='forget')
    
]
