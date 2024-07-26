from django.core.management.base import BaseCommand
from tasks.services.resource_allocation import priority_resource_allocation


class Command(BaseCommand):
    help = "Allocate stock to planned spare parts"

    def handle(self, *args, **kwargs):
        priority_resource_allocation()
        self.stdout.write(self.style.SUCCESS("Successfully resource allocated"))
