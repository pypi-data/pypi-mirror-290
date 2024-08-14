from django.conf import settings


def get_managed_pricing_plans():
    app_handle = settings.SHOPIFY_APP_HANDLE
    return f"https://admin.shopify.com/charges/{app_handle}/pricing_plans"


def update_or_create_charge_by_rest_data(shop, data):
    shop.billing.recurring_application_charges.update_or_create(
        shopify_rest_id=data["id"],
        defaults={
            "name": data["name"],
            "price": data["price"],
            "status": data["status"],
            "test": data["test"],
            "currency": data["currency"],
        },
    )


def activate_recuring_charge(shop, charge_id):
    print(f"Activating charge {charge_id} for shop {shop}")
    response = shop.get(
        f"/admin/api/api_version/recurring_application_charges/{charge_id}.json"
    )
    response.raise_for_status()
    charge = response.json()["recurring_application_charge"]
    update_or_create_charge_by_rest_data(shop, charge)
    return charge
