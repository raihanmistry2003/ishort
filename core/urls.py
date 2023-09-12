from django.urls import path, include
from .views import (
    home,
    dashboard,
    check_url,
    manage_urls,
    manage_plans,
    bulk_url_short,
    manage_qrcodes,
    check_out,
    payment_success,
    get_url_data,
    update_url,
    login_activities,
)

# app name ...
app_name = 'core'

urlpatterns = [
    #frontend Urls..
    path('', home, name='Home'),
    path('<slug>/', check_url, name="Check_Url"),

    # Dashboard Urls...
    path('user/dashboard/', dashboard, name="User_Dashboard"),
    path('user/manage-urls/', manage_urls, name="Manage_Urls"),
    path('user/manage-plan/', manage_plans, name="Manage_Plan"),
    path('user/bulk-url-short/', bulk_url_short, name="Bulk_Url_Short"),
    path('user/manage-qrs/', manage_qrcodes, name="Manage_QR_codes"),
    path('user/checkout/plan/', check_out, name="Check_Out"),
    path('user/payment/success/', payment_success, name="Payment_Success"),
    path('user/get_url_data/<id>', get_url_data, name="get_url_data"),
    path('user/update_url/<id>', update_url, name="update_url"),
    path('user/login/activities', login_activities, name="login_activities"),
    
]
