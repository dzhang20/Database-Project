from django.db import models

# Create your models here.
from catalog.models import UserProfile

class EventGroup(models.Model):
    name = models.CharField(max_length=100)
    brief = models.CharField(max_length=255,blank=True,null=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    admins = models.ManyToManyField(UserProfile,blank=True,related_name='group_admins')
    members = models.ManyToManyField(UserProfile,blank=True,related_name='group_members')
    capacity = models.IntegerField(default=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "eventgroups"
        verbose_name_plural = "eventgroups"
