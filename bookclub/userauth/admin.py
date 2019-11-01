from django.contrib import admin

# Register your models here
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('get_profile_id', 'id', 'username', 'email', 'get_gender', 'get_phone_number')
    list_select_related = ('profile',)

    def get_profile_id(self, instance):
        return instance.profile.id

    get_profile_id.short_description = 'Profile ID'

    def get_gender(self, instance):
        return instance.profile.gender

    get_gender.short_description = 'Gender'

    def get_phone_number(self, instance):
        return instance.profile.phone_number

    get_phone_number.short_description = 'Phone Number'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
