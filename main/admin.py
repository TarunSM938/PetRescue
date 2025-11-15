from django.contrib import admin
from .models import User, Pet, Request, ContactSubmission

# User Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')


# Pet Admin

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('pet_type', 'breed', 'status', 'owner', 'location', 'created_at')
    search_fields = ('pet_type', 'breed', 'location')
    list_filter = ('status', 'pet_type')



# Request Admin

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'request_type', 'phone_number', 'created_at')
    search_fields = ('user__username', 'pet__pet_type')
    list_filter = ('request_type',)


# Contact Submission Admin

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submission_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('status', 'submission_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
