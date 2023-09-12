from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.html import format_html
import razorpay
from django.conf import settings
from core.models import (
    User,
    Plan,
    Subscription,
    Payment,
    UserLoginHistory,
)
from functions.models import (
    Url,
    BulkUrlShort,
    QrCode,
    UrlHitDetail,
)
from functions.utils import (
    parse_csv_file,
)

from django.core.paginator import Paginator
from django.contrib.gis.geoip2 import GeoIP2
# Frontend View...

def check_url(request, slug):
    try:
        # Get the URL object associated with the short URL slug
        url_obj = get_object_or_404(Url, short_url=slug)

        # Create a UrlHitDetail instance to store hit details
        hit_detail = UrlHitDetail(url=url_obj)
        hit_detail.visitor_ip = request.META.get('REMOTE_ADDR')
        
        # Call the get_visitor_info() method to populate country and city
        hit_detail.get_visitor_info(request)

        # Call the parse_user_agent() method to populate browser and OS details
        hit_detail.parse_user_agent(request)

        hit_detail.hit_time = timezone.now()

        hit_detail.save()

        url_obj.url_hit_count = url_obj.url_hit_count+1
        url_obj.save()
        return redirect(url_obj.long_url)

    except Url.DoesNotExist:
        try:
            url_obj = BulkUrlShort.objects.get(short_url = slug)
            url_obj.url_hit_count = url_obj.url_hit_count+1
            url_obj.save()
            return redirect(url_obj.long_url)
        
        except BulkUrlShort.DoesNotExist:
            return redirect('core:Home')

def home(request):
    return render(request, 'index.html')



# Dashboard Views...

@login_required(login_url='account_login')
def dashboard(request):
    payment_obj = Payment.objects.filter(user = request.user).order_by('-timestamp')[:10]

    context = {
        'transctions':payment_obj,
    }
    return render(request,'Dashboard/index.html', context)


@login_required(login_url='account_login')
def manage_urls(request):
    subscrption = Subscription.objects.get(user = request.user)
    now = timezone.now()

    # Check if subscrption has expired or not
    if subscrption.expires_at < now:
        messages.error(request, f"dear, {request.user} your plan has been expired, Subscribe a new plan to continue our services.")
    
    if subscrption.used_urls < subscrption.plan.number_url:
        if request.method == "POST":
            long_url = request.POST['long_url']
            url_title = request.POST['url_title']
            url_create = Url.objects.create(
                user = request.user,
                long_url = long_url,
                url_title = url_title,
            )

            if url_create:
                subscrption.used_urls += 1
                subscrption.save()

                messages.success(request, f"Short url of {url_title} is created successfully.")
                return redirect('core:Manage_Urls')
            else:
                messages.error(request, f"Short url of {url_title} is not create yet, due to some issues!")
                return redirect('core:Manage_Urls')
    else:
        messages.error(request, format_html(f"Dear, {request.user} you have reached your limit as your active plan, if you want to access more of our features then subscribe our Premium plans from Manage Plans !"))

    url_obj = Url.objects.filter(user = request.user).order_by('-id')
    paginator = Paginator(url_obj, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'urls': page_obj,
    }

    return render(request, 'Dashboard/manage-urls.html', context)

@login_required(login_url='account_login')
def manage_plans(request):
    subscription_obj = Subscription.objects.get(user = request.user)
    plan_obj = Plan.objects.all()
    context = {
        "plans":plan_obj,
        "subscription": subscription_obj.plan.name
    }
    return render(request, 'Dashboard/plans.html', context)

@login_required(login_url='account_login')
def bulk_url_short(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        urls = parse_csv_file(excel_file)
        batch_size = 100
        total_urls = len(urls)
        shortened_urls = []

        for start_idx in range(0, total_urls, batch_size):
            end_idx = start_idx + batch_size
            batch_urls = urls[start_idx:end_idx]

            for url in batch_urls:
                short_url = BulkUrlShort.objects.create(user = request.user, long_url=url)
                shortened_urls.append(short_url)

            return render(request, 'Dashboard/bulk-url-short.html', {'shortened_urls': shortened_urls})
          
    return render(request, 'Dashboard/bulk-url-short.html')

@login_required(login_url='account_login')
def manage_qrcodes(request):
    subscrption = Subscription.objects.get(user = request.user)
    now = timezone.now()

    # Check if subscrption has expired or not
    if subscrption.expires_at < now:
        messages.error(request, f"dear, {request.user} your plan has been expired, Subscribe a new plan to continue our services.")

    if subscrption.used_qrs < subscrption.plan.number_qr:
        if request.method == "POST":
            long_url = request.POST['long_url']
            url_title = request.POST['url_title']
            qr_create = QrCode.objects.create(
                user = request.user,
                long_url = long_url,
                title = url_title,
            )

            if qr_create:
                subscrption.used_urls += 1
                subscrption.save()
                messages.success(request, f"QR code of {url_title} is created successfully.")
                return redirect('core:Manage_QR_codes')
            
            else:
                messages.error(request, f"QR code of {url_title} is not create yet, due to some issues!")
                return redirect('core:Manage_QR_codes')
    else:
        messages.error(request, format_html(f"Dear, {request.user} you have reached your limit as your active plan, if you want to access more of our features then subscribe our Premium plans from Manage Plans !"))

    qr_obj = QrCode.objects.filter(user = request.user)
    context = {
        'qrs': qr_obj,
    }

    return render(request, 'Dashboard/manage-qrs.html', context)

@login_required(login_url='account_login')
def check_out(request):
    if request.method == "POST":
        plan_obj = Plan.objects.get(id = request.POST['plan_id'])

        # Razorpay Gateway Settings --> 

        RAZOR_client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.RAZOR_KEY_SECRET))
        RAZOR_payment = RAZOR_client.order.create({'amount': plan_obj.price * 100, "currency" : "INR", "payment_capture":1})

        print(RAZOR_payment)

        subs_obj = Subscription.objects.get(user = request.user)
        subs_obj.razorpay_payment_id = RAZOR_payment['id']
        subs_obj.save()
    
    context = {
        'plan': plan_obj,
        'payment': RAZOR_payment,
    }
    return render(request, 'Dashboard/checkout.html', context)

@login_required(login_url="account_login")
def payment_success(request):
    order_id = request.GET.get('razorpay_order_id')
    subscription_obj = Subscription.objects.get(razorpay_payment_id = order_id)
    new_plan_id = Plan.objects.get(id = request.GET.get('plan_id'))
    subscription_obj.user = request.user
    subscription_obj.plan = new_plan_id
    subscription_obj.save()

    Payment.objects.create(
        user = request.user,
        plan = new_plan_id,
        payment_id = subscription_obj.razorpay_payment_id,
        amount = subscription_obj.plan.price,
        payment_status = 'success',
    )

    return render(request, 'Dashboard/payment-success.html')


def get_url_data(request, id):
    url_obj = Url.objects.get(id = id)

    data = {
        'short_url': url_obj.short_url,
        'url_title': url_obj.url_title,
        'long_url' : url_obj.long_url,
    }
    print(data)
    return JsonResponse(data)


def update_url(request, id):
    if request.method == "POST":
        url_obj = Url.objects.get(id = id)
        short_url = request.POST['short_url']
        url_title = request.POST['url_title']

        if url_obj:
            url_obj.short_url = short_url
            url_obj.url_title = url_title
            url_obj.save()
            return JsonResponse({'success':True})
    
    return JsonResponse({'success':False})

def login_activities(request):
    login_history_obj = UserLoginHistory.objects.filter(user = request.user).order_by('-id')
    paginator = Paginator(login_history_obj, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'activities' : page_obj
    }
    return render(request, 'Dashboard/login-activities.html', context)