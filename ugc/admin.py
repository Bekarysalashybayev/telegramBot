from django.contrib import admin

from .forms import ProfileForm
from .models import Profile, Message, Deposit


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'button_value')
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')


@admin.register(Deposit)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'sum', 'deadline', 'emonth')