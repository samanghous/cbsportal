from django.contrib import admin
from cbs_portal.models import SecurityKeymodel,UserComplaint,UserMessFeedback,NewsEvents
 
# Register your models here.
admin.site.register(SecurityKeymodel)
admin.site.register(UserComplaint)
admin.site.register(UserMessFeedback)
admin.site.register(NewsEvents)
