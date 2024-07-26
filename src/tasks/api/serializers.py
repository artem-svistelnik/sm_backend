from rest_framework.fields import ReadOnlyField
from rest_framework.fields import (
    SerializerMethodField,
    IntegerField,
    DateTimeField,
    ChoiceField,
)
from rest_framework.serializers import ModelSerializer, Serializer

from tasks.models import PlannedSparePart, StatusTaskTypes, Task, SparePart


class SparePartSerializer(ModelSerializer):
    class Meta:
        model = SparePart
        fields = (
            "id",
            "name",
            "measurement_units",
            "price",
        )


class PlannedSparePartSerializer(ModelSerializer):
    spare_part = SerializerMethodField("get_spare_part")

    class Meta:
        model = PlannedSparePart
        fields = (
            "id",
            "planned_count",
            "in_stock",
            "spare_part",
        )

    def get_spare_part(self, instance: PlannedSparePart):
        return SparePartSerializer(instance.spare_part).data


class TaskSerializer(ModelSerializer):
    planned_spare_parts = SerializerMethodField(
        "get_planned_spare_parts", read_only=True
    )
    id = IntegerField(read_only=True)
    created_at = DateTimeField(read_only=True)
    author = ReadOnlyField(source="author.id")

    class Meta:
        model = Task
        fields = (
            "id",
            "status",
            "description",
            "created_at",
            "executed_at",
            "scheduled_date",
            "author",
            "executor",
            "planned_spare_parts",
        )

    def get_planned_spare_parts(self, instance: Task):
        return PlannedSparePartSerializer(
            instance.planned_spare_parts.all(), many=True
        ).data


class CreateSparePartSerializer(ModelSerializer):
    class Meta:
        model = PlannedSparePart
        fields = ("spare_part", "planned_count")


class CreateTaskSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    author = ReadOnlyField(source="author.id")
    planned_spare_parts = CreateSparePartSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "description",
            "scheduled_date",
            "author",
            "executor",
            "planned_spare_parts",
        )


class EditTaskSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    planned_spare_parts = CreateSparePartSerializer(many=True, read_only=True)
    author = ReadOnlyField(source="author.id")

    class Meta:
        model = Task
        fields = (
            "id",
            "description",
            "scheduled_date",
            "executor",
            "author",
            "planned_spare_parts",
        )


class ChangeStatusTaskSerializer(Serializer):
    status = ChoiceField(choices=StatusTaskTypes.choices)


class UpdatePlannedSparePartSerializer(Serializer):
    planned_spare_parts = CreateSparePartSerializer(many=True)
