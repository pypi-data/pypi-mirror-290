from django.contrib import admin

from .models import ShopBilling, RecurringApplicationCharge


@admin.register(ShopBilling)
class ShopBillingAdmin(admin.ModelAdmin):
    readonly_fields = ("shop",)


@admin.register(RecurringApplicationCharge)
class RecurringApplicationChargeAdmin(admin.ModelAdmin):
    list_display = ("name", "shop_billing", "price", "status", "test", "currency")
    list_filter = ("status", "test")
