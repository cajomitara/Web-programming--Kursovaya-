from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [
    # публичный API (пути совпадают со старыми, поэтому frontend не меняется)
    path('api/users/login/', views.login_view),
    path('api/users/logout/', views.logout_view),
    path('api/users/my/', views.my_view),

    # внутренний API для других сервисов
    path('internal/users/', views.internal_create_user),
    path('internal/users/<int:user_id>/', views.internal_update_user),

    # проверки состояния
    path('health/live/', views.health_live),
    path('health/ready/', views.health_ready),

    # админка для управления пользователями
    path('auth/admin/', admin.site.urls),
]
