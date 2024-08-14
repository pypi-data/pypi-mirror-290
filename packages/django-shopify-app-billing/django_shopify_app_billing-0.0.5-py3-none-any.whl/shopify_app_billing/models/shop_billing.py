from django.db import models
from django.conf import settings

from ..services import get_managed_pricing_plans


class ShopBilling(models.Model):

    class Meta:
        verbose_name = "Shop Billing"
        verbose_name_plural = "Shops Billing"

    def __str__(self):
        return f"billing for {self.shop.shopify_domain}"

    @property
    def managed_pricing_plans_url(self):
        return get_managed_pricing_plans()
