from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Package, Booking, Contact  # <--- Contact Model Import kiya
from django.db.models import Q

# 👇 Email bhejne ke liye ye 2 line zaroori hain
from django.core.mail import send_mail
from django.conf import settings

# --- AUTH VIEWS (Login/Signup/Logout) ---

def landing_page(request):
    packages = Package.objects.all()[:3]
    return render(request, 'landing.html', {'packages': packages})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

# --- MAIN APP LOGIC ---

@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('q')
    if query:
        packages = Package.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        packages = Package.objects.all()
    
    my_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'packages': packages, 'my_bookings': my_bookings})

@login_required(login_url='login')
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == "POST":
        date = request.POST.get('date')
        
        # 1. Booking Create Karo
        booking = Booking.objects.create(
            user=request.user, 
            package=package, 
            booking_date=date,
            status='Confirmed' # Status dena zaroori hai admin color ke liye
        )

        # 2. EMAIL SENDING LOGIC 📧 (Ye naya code hai)
        subject = f"Booking Confirmed: Trip to {package.name}"
        message = f"""
        Hi {request.user.username},

        Congratulations! Your trip to {package.name} is confirmed.
        
        Details:
        - Package: {package.name}
        - Price: Rs. {package.price}
        - Date: {date}
        - Booking ID: #{booking.id}

        You can download your ticket from your dashboard.
        
        Happy Travelling!
        Team TravelManager
        """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email, ]
        
        # Try-Except taaki agar internet na ho to error na aaye
        try:
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(f"Email Error: {e}") 

        # Success page par user ka naam bhejo
        return render(request, 'success.html', {'name': request.user.username})
    
    return render(request, 'booking_form.html', {'package': package})

@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        booking.delete()
        return redirect('dashboard')
    return render(request, 'confirm_cancel.html', {'booking': booking})

@login_required(login_url='login')
def ticket_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'ticket.html', {'booking': booking})

# --- CONTACT FORM LOGIC ---
# Imports sabse upar hone chahiye
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact

def contact_view(request):
    if request.method == "POST":
        # 1. Form se data nikalo
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # 2. Database me save karo (Record ke liye)
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        
        # 3. Email Body taiyar karo
        email_subject = f"New Contact: {subject}"
        email_message = f"""
        Hello Admin,

        You have received a new message from your website.

        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        
        -----------------------
        TravelManager Notification System
        """
        
        # 4. Email Send karo (Try-Except taaki error na aaye)
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,  # Bhejne wala (Aap)
                [settings.EMAIL_HOST_USER], # Paane wala (Aap khud hi)
                fail_silently=False,
            )
            print("Email sent successfully!") # Console me dikhega
        except Exception as e:
            print(f"Email Error: {e}") # Agar net nahi chala to yahan error dikhega

        # 5. Success page dikhao
        return render(request, 'contact.html', {'success': True})
    
    # Agar GET request hai to bas form dikhao
    return render(request, 'contact.html')

def about_view(request):
    return render(request, 'about.html')