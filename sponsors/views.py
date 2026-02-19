import json
from django.shortcuts import render, redirect
from .models import hightea, Payment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import calendar
from django.http import JsonResponse
import razorpay
from django.conf import settings
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


client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        date_str = data.get('date')
        sponsor_name = data.get('sponsor_name')
        contact = data.get('contact')
        amount = int(data.get('amount')) * 100

        date_obj = datetime.strptime(date_str, "%b. %d, %Y")
        sunday_date = date_obj.strftime("%Y-%m-%d")
        
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": '1'
        })

        Payment.objects.create(
            user=request.user,
            razorpay_order_id=razorpay_order['id'],
            amount=amount,
            status='Created',
            sponsor_name=sponsor_name,
            contact=contact,
            sunday_date=sunday_date
        )

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "amount": amount,
            "key": settings.RAZOR_KEY_ID
        })
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        try:
            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Signature valid → payment successful
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = "Success"
            payment.save()

            # Now create booking (only after payment success)
            hightea.objects.create(
                sunday_date=payment.sunday_date,
                sponsor_name=payment.sponsor_name,
                contact=payment.contact,
                status="Booked",
                booked_by=payment.user
            )

            return JsonResponse({"status": "success"})

        except razorpay.errors.SignatureVerificationError:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.status = "Failed"
            payment.save()

            return JsonResponse({"status": "failed"})

