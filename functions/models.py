from django.utils import timezone
from django.db import models
from .validators import validate_xlsx_extension
from core.models import (
    User
)
import random
import string
import qrcode
from django.contrib.gis.geoip2 import GeoIP2
import user_agents
from io import BytesIO
from django.core.files import File

# Create your models here.

class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    short_url = models.CharField(max_length = 20, blank=True, verbose_name="Short Url Auto Generated")
    long_url = models.TextField(verbose_name="Long Url")
    url_title = models.CharField(max_length=100, verbose_name="Url Title")
    url_hit_count = models.PositiveIntegerField(default=0, verbose_name="Url Hit Count")
    url_created_at = models.DateField(auto_now=True)
    url_updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.short_url

    def save(self, *args, **kwargs):
        random_short = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        self.short_url = str(random_short)
        super(Url, self).save(*args, **kwargs)


class UrlHitDetail(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name='urls')
    visitor_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Visitor IP")
    country = models.CharField(max_length=2, blank=True, null=True, default="N/A", verbose_name="Country Code")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    hit_time = models.DateTimeField(null=True, blank=True, verbose_name="Hit Time")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    browser = models.CharField(max_length=100, blank=True, verbose_name="Browser")
    os = models.CharField(max_length=100, blank=True, verbose_name="Operating System")

    def save(self, *args, **kwargs):
        if not self.visitor_ip or not self.country:
            # Get visitor's IP address and country
            self.visitor_ip, self.country, self.city = self.get_visitor_info()
            self.hit_time = timezone.now()

        if not self.browser or not self.os:
            # Parse and extract browser and OS details from User Agent
            self.parse_user_agent()

        super(UrlHitDetail, self).save(*args, **kwargs)

    def get_visitor_info(self, request=None):
        # Get the visitor's IP address from the request object if provided
        visitor_ip = None

        if request:
            visitor_ip = request.META.get('REMOTE_ADDR')

        try:
            g = GeoIP2()
            country = g.country(visitor_ip)['country_code']
            city = g.city(visitor_ip)['city']
        except Exception as e:
            # Handle exceptions if GeoIP lookup fails
            country = None
            city = None

        return visitor_ip, country, city
    
    def parse_user_agent(self, request):
        # Extract browser and OS details from User Agent
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')

        if user_agent_string:
            user_agent = user_agents.parse(user_agent_string)
            self.browser = user_agent.browser.family
            self.os = user_agent.os.family


class ExcelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    excelsheet = models.FileField(upload_to='Excel_Files', max_length=100, verbose_name="Upload Excel Sheet", validators=[validate_xlsx_extension])
    created_at = models.DateField(auto_now=True)

class BulkUrlShort(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    short_url = models.CharField(max_length = 20, blank=True, verbose_name="Short Url Auto Generated")
    long_url = models.TextField(verbose_name="Long Url")
    url_title = models.CharField(max_length=250, null=True, blank=True, verbose_name="Url Related Title")
    url_hit_count = models.PositiveIntegerField(default=0, verbose_name="Url Hit Count")
    url_created_at = models.DateField(auto_now=True)
    url_updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        random_short = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        self.short_url = str(random_short)
        super(BulkUrlShort, self).save(*args, **kwargs)

class QrCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    long_url = models.TextField()
    title = models.CharField(max_length=100)
    qrcode = models.ImageField(upload_to='Qrcodes', null=True, blank='True', verbose_name="Qr code Auto Generated")
    created_at = models.DateField(auto_now=True)

    # save method
    def save(self, *args, **kwargs):
        my_qr = qrcode.make(self.long_url)
        file_name = f'{self.user}-{self.title}qr.png'
        stream = BytesIO()
        my_qr.save(stream, 'PNG')
        self.qrcode.save(file_name, File(stream), save=False)
        super().save(*args, **kwargs)
    