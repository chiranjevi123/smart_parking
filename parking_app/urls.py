from django.urls import path
from .views import select_parking_area, select_slot, proceed_to_payment, booking_confirmation, qr_scanner_view, scan_qr_result   # Ensure select_slot exists
urlpatterns = [
    path('select-parking-area/', select_parking_area, name='select_parking_area'),
    path('select-slot/<int:parking_area_id>/', select_slot, name='select_slot'),
    path('proceed-to-payment/<int:slot_id>/', proceed_to_payment, name='proceed_to_payment'),
    path('booking-confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path("scan_qr/", qr_scanner_view, name="qr_scanner"),
       path('scan_qr_result/', scan_qr_result, name='scan_qr_result'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

