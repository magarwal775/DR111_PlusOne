from django.contrib import admin
from chat.models import Messages, Group
# Register your models here.

class MessagesAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in Messages._meta.get_fields()]

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

class GroupAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in Group._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

admin.site.register(Messages, MessagesAdmin)
admin.site.register(Group)