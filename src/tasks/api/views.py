from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from tasks.api.serializers import (
    ChangeStatusTaskSerializer,
    CreateTaskSerializer,
    EditTaskSerializer,
    TaskSerializer,
    UpdatePlannedSparePartSerializer,
)
from tasks.models import (
    PlannedSparePart,
    StatusTaskTypes,
    Task,
)


class TaskView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Task.objects.all().order_by("created_at")
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.create(
            description=serializer.validated_data["description"],
            scheduled_date=serializer.validated_data["scheduled_date"],
            author=request.user,
            executor=serializer.validated_data["executor"],
        )
        task.save()
        PlannedSparePart.objects.bulk_create(
            [
                PlannedSparePart(
                    task_id=task.id,
                    spare_part_id=i.get("spare_part"),
                    planned_count=i.get("planned_count"),
                )
                for i in serializer.data.get("planned_spare_parts")
            ]
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveTaskView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = EditTaskSerializer
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskStatusesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        statuses = [i for i in StatusTaskTypes]
        return Response(statuses)


class ChangeStatusesView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = ChangeStatusTaskSerializer

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        task.status = serializer.validated_data["status"]
        task.save()
        return Response(serializer.data)


class UpdatePlannedSparePartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        serializer = UpdatePlannedSparePartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PlannedSparePart.objects.filter(task_id=task_id).delete()
        PlannedSparePart.objects.bulk_create(
            [
                PlannedSparePart(
                    task_id=task_id,
                    spare_part_id=i.get("spare_part"),
                    planned_count=i.get("planned_count"),
                )
                for i in serializer.data.get("planned_spare_parts")
            ]
        )

        return Response(serializer.data)
