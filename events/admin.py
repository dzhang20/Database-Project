from django.contrib import admin

# Register your models here.
from .models import events, Review, Cluster

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('bussiness', 'rating', 'user_id', 'comment', 'date')
    list_filter = ['date', 'user_id']
    search_fields = ['comment']
class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']
admin.site.register(events)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
