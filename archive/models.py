from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
# Create your models here.


class District(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(_('slug'),max_length=70, null=True, unique=True)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = ('Districts')
        ordering = ['name']

    def __str__(self):
        return self.name



class Dalal(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('captured', 'Captured'),
        ('fugitive', 'Fugitive'),
        ('terminated', 'Terminated'),
        ('unknown', 'Unknown'),
    ]

    name = models.CharField(max_length=250)
    dalal_code = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to='dalals/pictures/', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    #Identity
    # dob = models.DateField(null=True, blank=True)
    address_last_known = models.TextField(null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)

    #public info
    role = models.CharField(max_length=250)
    affiliation = models.TextField()
    profile_report = RichTextField(blank=True, null=True)

    #metrics
    traitor_rank  = models.IntegerField(default=1, validators=(MinValueValidator(1), MaxValueValidator(100)))
    shoe_count = models.PositiveIntegerField(default=0)

    date_added = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='unknown')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


