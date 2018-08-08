from django.db import models
import numpy as np
from django.contrib.auth.models import User
# Create your models here.

class events(models.Model):
    business_id = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)
    keyword = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    city=models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    founder=models.CharField(max_length=100,null=True, blank=True)
    review_count = models.FloatField(null=True, blank=True)
    stars = models.FloatField(null=True, blank=True)
    #latitude=models.FloatField(null=True, blank=True)
    #longitude=models.FloatField(null=True, blank=True)
    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)
    class Meta:
        indexes=[
            models.Index(
                fields=['keyword','city'],
                name='key_city_index'
            )
        ]

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    review_id = models.CharField(max_length = 200,primary_key= True)
    bussiness = models.ForeignKey(events,on_delete=models.SET_NULL, null = True)
    date = models.DateTimeField('date published')
    user_id = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)

class Cluster(models.Model):
    name = models.CharField(max_length=100,null=True)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
