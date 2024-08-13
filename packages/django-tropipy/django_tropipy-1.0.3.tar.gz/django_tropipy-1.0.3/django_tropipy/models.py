from django.db import models

class TropipayOrder(models.Model):
    uuid = models.CharField(max_length=255, unique=True, primary_key=True, verbose_name='UUID')
    title = models.CharField(max_length=255, verbose_name='Title')
    name = models.CharField(max_length=255, verbose_name='Name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(max_length=255, verbose_name='Phone number')
    description = models.TextField(verbose_name='Description')
    location = models.CharField(max_length=255, verbose_name='Location')
    total = models.FloatField(verbose_name='Total')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return self.uuid

    class Meta:
        verbose_name = 'Tropipay Order'
        verbose_name_plural = 'Tropipay Orders'
        ordering = ['-created_at']