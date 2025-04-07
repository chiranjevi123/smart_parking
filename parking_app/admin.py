from django.contrib import admin
from .models import ParkingArea, ParkingSlot, ParkingRecord

admin.site.register(ParkingArea)
admin.site.register(ParkingSlot)
admin.site.register(ParkingRecord)
