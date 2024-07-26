from django.contrib import admin

from tasks.models import StockBalance, SparePart


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_units", "price")
    search_fields = ("id", "name")


@admin.register(StockBalance)
class StockBalanceAdmin(admin.ModelAdmin):
    list_display = ("id", "stock", "count", "spare_part")
    list_filter = ("spare_part",)
    search_fields = ("id", "stock")
