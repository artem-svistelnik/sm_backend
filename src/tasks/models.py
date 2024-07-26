from django.db import models
from django.contrib.auth.models import User


class StatusTaskTypes(models.TextChoices):
    """status of task enum"""

    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    UNDER_REVIEW = "UNDER_REVIEW"
    DONE = "DONE"


class Task(models.Model):
    status = models.CharField(
        max_length=20,
        choices=StatusTaskTypes.choices,
        default=StatusTaskTypes.PLANNED,
    )
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateField(null=True, blank=True)
    scheduled_date = models.DateField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="author_of_tasks", null=True
    )
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="executor_of_tasks", null=True
    )

    def __str__(self):
        return f"Task № {self.id} : {self.description[:20]}"


class SparePart(models.Model):
    name = models.CharField(max_length=255)
    measurement_units = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    similar_spare_parts = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.name


class PlannedSparePart(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="planned_spare_parts"
    )
    spare_part = models.ForeignKey(
        SparePart, on_delete=models.CASCADE, related_name="planned"
    )
    planned_count = models.PositiveIntegerField(default=0)
    in_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Task № {self.task.id}; spare part : {self.spare_part.name}"


class StockBalance(models.Model):
    spare_part = models.ForeignKey(
        SparePart, on_delete=models.CASCADE, related_name="stock", null=True
    )
    count = models.PositiveIntegerField(default=0)
    stock = models.CharField(max_length=100)

    def __str__(self):
        return f"stock :{self.stock}; spare part : {self.spare_part.name}, count : {self.count}"
