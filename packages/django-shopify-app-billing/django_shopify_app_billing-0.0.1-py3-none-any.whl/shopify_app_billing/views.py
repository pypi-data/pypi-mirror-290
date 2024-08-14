from django.http import HttpResponse
from django.shortcuts import redirect, render

from .services import get_managed_pricing_plans, activate_recuring_charge

from shopify_app.decorators import shop_session


def plans_redirect(request):
    return redirect(get_managed_pricing_plans())


@shop_session
def activate_plan(request, *args, **kwargs):

    shop = request.shop
    recurring_charge_id = request.GET.get("charge_id")
    if not shop or not recurring_charge_id:
        return redirect("shopify_app_billing:plans")

    plan = activate_recuring_charge(shop, recurring_charge_id)

    if plan["status"] == "active":
        return redirect("/plan-activated/")
    else:
        return redirect("shopify_app_billing:plans")
