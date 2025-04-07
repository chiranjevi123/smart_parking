from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from parking_app.models import ParkingRecord, ParkingSlot, ParkingArea

from .forms import BookingForm

from django.db import IntegrityError

from django.http import JsonResponse
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


def home(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    return render(request, 'registration.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user_type = request.POST.get("user_type", "user")  # Default to 'user'

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        
        if user_type == "admin":
            user.is_staff = True  # Admin privileges
            user.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, "registration.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if user.is_staff:  # Redirect admins to admin dashboard
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')  # Redirect regular users to user dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')  # Redirect admins to their dashboard

    parking_history = ParkingRecord.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'parking_history': parking_history})

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    parking_records = ParkingRecord.objects.all()
    total_users = User.objects.count()
    booked_slots = ParkingSlot.objects.filter(is_booked=True).count()
    available_slots = ParkingSlot.objects.filter(is_booked=False).count()

    context = {
        'parking_records': parking_records,
        'total_users': total_users,
        'booked_slots': booked_slots if booked_slots is not None else 0,
        'available_slots': available_slots if available_slots is not None else 0,

    }
    return render(request, 'admin_dashboard.html', context)



def add_parking_area(request):
    if request.method == "POST":
        name = request.POST.get('name')
        total_slots = request.POST.get('total_slots')
        price_per_slot = request.POST.get('price_per_slot')
        ParkingArea.objects.create(name=name, total_slots=total_slots, price_per_slot=price_per_slot)
        messages.success(request, "Parking Area Added Successfully!")
    return redirect('manage_parking_areas')


def edit_parking_area(request):
    if request.method == "POST":
        area_id = request.POST.get('area_id')
        name = request.POST.get('name')
        total_slots = request.POST.get('total_slots')
        price_per_slot = request.POST.get('price_per_slot')
        ParkingArea.objects.filter(id=area_id).update(name=name, total_slots=total_slots, price_per_slot=price_per_slot)
        messages.success(request, "Parking Area Updated Successfully!")
    return redirect('manage_parking_areas')

def delete_parking_area(request, area_id):
    ParkingArea.objects.filter(id=area_id).delete()
    messages.success(request, "Parking Area Deleted Successfully!")
    return redirect('manage_parking_areas')


@login_required
def manage_slots(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    slots = ParkingSlot.objects.all()
    return render(request, 'manage_slots.html', {'slots': slots})

@login_required
def view_bookings(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    bookings = ParkingRecord.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})

@login_required
def update_slot_status(request, slot_id):
    if request.method == "POST":
        slot = get_object_or_404(ParkingSlot, id=slot_id)
        slot.status = request.POST.get('status')
        slot.save()
        messages.success(request, "Slot status updated successfully!")
    return redirect('manage_slots')

@login_required
def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(ParkingRecord, id=booking_id)
        booking.status = 'canceled'
        booking.save()
        messages.success(request, "Booking canceled successfully!")
    return redirect('view_bookings')


def manage_parking_areas(request):
    parking_areas = ParkingArea.objects.all()  # Fetch all parking areas
    print(parking_areas)  # Debugging step to check if data is being fetched
    return render(request, 'manage_parking_areas.html', {'parking_areas': parking_areas})

def book_slot(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('generate_qr', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'book_slot.html', {'form': form})


def dashboard(request):
    parking_history = ParkingRecord.objects.filter(user=request.user).order_by('-entry_time')
    return render(request, 'dashboard.html', {'parking_history': parking_history})




def select_parking_area(request):
    if request.method == "POST":
        # Get selected date and time from form
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")

        # Fetch only active parking areas
        parking_areas = ParkingArea.objects.filter(is_active=True)

        # Store date and time in session (to pass to the next step)
        request.session["booking_date"] = booking_date
        request.session["booking_time"] = booking_time

        return render(request, "select_parking_area.html", {"parking_areas": parking_areas})

    return redirect("dashboard")  # If accessed without POST request, go back to dashboard



def select_slot(request, parking_area_id):
    parking_area = get_object_or_404(ParkingArea, id=parking_area_id)

    # Fetch existing slots for the parking area
    existing_slots = ParkingSlot.objects.filter(parking_area=parking_area).count()

    # If no slots exist, create them dynamically based on admin input
    if existing_slots == 0:
        for i in range(1, parking_area.total_slots + 1):  # Start numbering from 1 per parking area
            try:
                ParkingSlot.objects.create(
                    parking_area=parking_area,
                    slot_number=i,  # Slot numbers reset for each parking area
                    is_booked=False
                )
            except IntegrityError:
                print(f"Slot {i} already exists in {parking_area.name}, skipping.")

    # Fetch updated slot list for the parking area
    slots = ParkingSlot.objects.filter(parking_area=parking_area).order_by('slot_number')

    return render(request, 'select_slot.html', {'parking_area': parking_area, 'slots': slots})

def proceed_to_payment(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)

    if request.method == "POST":
        # Simulating a successful payment (Replace this with actual payment gateway integration)
        payment_successful = True

        if payment_successful:
            # Create a new booking record
            booking = ParkingRecord.objects.create(
                user=request.user,
                slot=slot,
                entry_time=timezone.now(),
                status="booked"
            )

            # Mark the slot as booked
            slot.is_booked = True
            slot.save()

            # Generate QR Code
            qr = qrcode.make(f"User: {request.user.username}, Slot: {slot.slot_number}, Area: {slot.parking_area.name}")
            qr_io = BytesIO()
            qr.save(qr_io, format='PNG')
            booking.qr_code.save(f"qr_{booking.id}.png", ContentFile(qr_io.getvalue()), save=True)

            return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, "payment.html", {"slot": slot})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(ParkingRecord, id=booking_id, user=request.user)
    return render(request, "booking_confirmation.html", {"booking": booking})





from django.contrib.admin.views.decorators import staff_member_required
from urllib.parse import unquote

@staff_member_required  # Admin-only access
def qr_scanner_view(request):
    return render(request, "qr_scanner.html")








@login_required
def scan_qr_result(request):
    data = request.GET.get('data')
    return render(request, 'scan_result.html', {'data': data})