from django.db import models
from django.contrib.auth.models import User
import datetime


class Product(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    url = models.TextField()
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    pub_date = models.DateTimeField()
    votes_total = models.IntegerField(default = 1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def summary(self):
        return self.body[:300]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



# default='http://127.0.0.1:8000/media/images/boxed-water-is-better-1464023-unsplash_Xvyfo9M.jpg'
