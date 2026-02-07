from django.contrib import admin
from django.urls import path
from main_app import views

# 👇 YEH LINE SABSE ZAROORI HAI (Iske bina error aayega)
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth & Public
    path('', views.landing_page, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # App Logic
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('ticket/<int:booking_id>/', views.ticket_view, name='ticket_view'),
    
    # Password Change URLs (Ab ye chalega kyunki upar import laga diya hai)
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('contact/', views.contact_view, name='contact'),
    # urlpatterns list ke andar:
path('about/', views.about_view, name='about'),
]