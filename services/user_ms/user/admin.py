# Core Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _
# Imports from your apps
from profiles.models import User

from oauth2_provider.models import AccessToken, Application, Grant, \
    RefreshToken


class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True


class MyUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


class MyUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass


class UserModelAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'email',)
    filter_horizontal= ['user_permissions', 'groups']
    add_fieldsets = (
        (
            None,
            {
                'fields': ('username', 'email', 'password1', 'password2'),
                'classes': ('wide',)
            }
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        (_('extrafields'), {'fields': ('photo', 'phone', 'cell_phone', 
        'document_number', 'type_document', 'specialty', 'charge', 
        'city', 'country', 'company_area', 'company', 'address')}),
    )
    #import pdb; pdb.set_trace()

admin.site.register(User, UserModelAdmin)


class PermissionModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'codename']


admin.site.register(Permission, PermissionModelAdmin)

admin.site.register(Group)

admin.site.register(AccessToken)
admin.site.register(Application)
admin.site.register(Grant)
admin.site.register(RefreshToken)