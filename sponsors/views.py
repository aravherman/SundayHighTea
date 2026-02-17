from django.shortcuts import render, redirect
from .models import hightea
from django.contrib.auth import authenticate, login, logout
import calendar
from datetime import date, datetime
# Create your views here.

def home(request):
    return render(request, 'sponsors/home.html')

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        
        print("USERNAME:", uname)
        print("PASSWORD:", upass)
        user = authenticate(request, username=uname, password=upass)
        print("USER:", user)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'bs/login.html', {'error': 'Invalid user or password'})
    return render(request, 'bs/login.html')

def dashboard(request):
    year = date.today().year
    months = []

    bookings = hightea.objects.all()
    booking_dict = {b.sunday_date: b for b in bookings}

    for month in range(1, 13):
        sundays = []
        cal = calendar.monthcalendar(year, month)

        for week in cal:
            if week[calendar.SUNDAY] != 0:
                d = date(year, month, week[calendar.SUNDAY])

                if d in booking_dict:
                    sundays.append({
                        "date": d,
                        "booked": True,
                        "status": booking_dict[d].status
                    })
                else:
                    sundays.append({
                        "date": d,
                        "booked": False,
                        "status": "Available"
                    })

        months.append({
            "name": calendar.month_name[month],
            "sundays": sundays
        })

    return render(request, "sponsors/dashboard.html", {
        "months": months,
        "year": year
    })

def book_hightea(request):
    if request.method == 'POST':
        date = request.POST.get('date')

        date_obj = datetime.strptime(date, "%b. %d, %Y")
        fdate = date_obj.strftime("%Y-%m-%d")

        sponsor_name = request.POST.get('sponsor_name')
        contact = request.POST.get('contact')
        hightea.objects.update_or_create(
            sunday_date=fdate,
            defaults={
                "sponsor_name": sponsor_name,
                "contact": contact,
                "status": "Booked",
                "booked_by": request.user
            }
        )
    return redirect("dashboard")
    
