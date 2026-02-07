from django.contrib import admin
from .models import Package, Booking, Contact # <--- Yahan Contact add kiya hai
from django.utils.html import format_html

# 1. Package Admin
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'days', 'image_preview')
    search_fields = ('name', 'description')
    list_filter = ('days',)

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height:50px; border-radius:5px;" />', obj.image_url)
        return "-"
    image_preview.short_description = 'Image Preview'

# 2. Booking Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'booking_date', 'status', 'created_at')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'package__name')
    list_editable = ('status',) 

# 3. Contact Admin (NEW: Messages padhne ke liye) 📬
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at') # Ye columns dikhenge
    search_fields = ('name', 'email', 'subject') # Search kar sakoge
    list_filter = ('sent_at',) # Date wise filter
    readonly_fields = ('message',) # Message sirf padh sako, edit na ho

# Models Register Karna
admin.site.register(Package, PackageAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Contact, ContactAdmin) # <--- Contact register ho gaya

# Branding
admin.site.site_header = "TravelManager Admin"
admin.site.site_title = "Travel Admin Portal"
admin.site.index_title = "Welcome to TravelManager Control Room"