from django.contrib import admin
from django.contrib.auth.models import Group

from oauth2_provider.models import AccessToken, Application, Grant, \
    RefreshToken, IDToken

admin.site.unregister(Group)

admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
admin.site.unregister(IDToken)
