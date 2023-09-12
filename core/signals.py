from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Plan, Subscription, User
from datetime import datetime, timedelta

@receiver(post_save, sender = User)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        print('subscription created')
        default_plan = Plan.objects.get(name = "Basic")
        expires_at = datetime.now() + timedelta(days = default_plan.duration)
        subscription_obj = Subscription(user = instance, plan = default_plan, expires_at = expires_at)
        subscription_obj.subs_count += 1
        subscription_obj.save()
