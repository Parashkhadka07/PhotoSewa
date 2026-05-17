from django.shortcuts import render, get_object_or_404, redirect
from packages.models import Package
from .forms import BookingForm
from .models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def book_package(request, pkg_id):
    pkg = get_object_or_404(Package, id=pkg_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check duplicate before saving
            already_booked = Booking.objects.filter(
                client=request.user.email,
                package=pkg
            ).exists()

            if already_booked:
                messages.error(request,"You already requested this package!")
                return redirect("home_page")
            else:
                booking = form.save(commit=False)
                booking.package = pkg
                booking.client = request.user.email
                booking.photographer = pkg.photographer.user.email
                booking.price = pkg.price
                booking.cameras = pkg.no_of_cameras or 0
                booking.staff = pkg.no_of_staffs or 0
                booking.drone = pkg.drone_included
                booking.Accessories = pkg.free_accessories or ''
                booking.save()
                messages.success(request,"Booking Requested Sucessfully")
                return redirect('profile_page')
    else:
        form = BookingForm()

        

    return render(request, 'bookings/book_package.html', {'pkg': pkg, 'form': form})



@login_required
def my_bookings(request):
    email = request.user.email
    is_photographer = request.user.user_role == 'photographer'

    if is_photographer:
        bookings = Booking.objects.filter(
            photographer=email
        ).exclude(status=Booking.Status.CANCELLED).order_by('-date_of_booking').select_related('package')
    else:
        bookings = Booking.objects.filter(
            client=email
        ).exclude(status=Booking.Status.CANCELLED).order_by('-date_of_booking').select_related('package')

    context = {
        'bookings': bookings,
        'is_photographer': is_photographer,
        'pending_count': bookings.filter(status=Booking.Status.PENDING).count(),
        'confirmed_count': bookings.filter(status=Booking.Status.CONFIRMED).count(),
    }
    return render(request, 'bookings/my_bookings.html', context)

@login_required
def update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    email = request.user.email

    if action == 'confirm' and booking.photographer == email:
        booking.status = Booking.Status.CONFIRMED
        booking.save()  # only save here
        messages.success(request, "Booking confirmed.")

    elif action == 'reject':
        booking.delete()
        messages.success(request, "Booking rejected.")

    elif action == 'cancel':
        booking.delete()
        messages.success(request, "Booking cancelled.")

    else:
        messages.error(request, "Unauthorized action.")

    return redirect('my_bookings')