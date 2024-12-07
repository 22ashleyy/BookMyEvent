from django.db import models

# Create your models here.
class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('concert', 'Concert'),
        ('family', 'Family'),
        ('theatre', 'Theatre'),
        ('sport', 'Sport'),
    ]
    title = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    amount = models.CharField(max_length=10)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='concert')

    def __str__(self):
        return self.title
