from tasks.models import StockBalance, PlannedSparePart, StatusTaskTypes


def priority_resource_allocation():
    planned_spare_parts = PlannedSparePart.objects.filter(
        task__status=StatusTaskTypes.PLANNED
    ).order_by("task__created_at")
    for planned_spare_part in planned_spare_parts:
        similar_spare_parts = list(
            planned_spare_part.spare_part.similar_spare_parts.values_list(
                "id", flat=True
            )
        )
        spare_parts_balances = StockBalance.objects.filter(
            spare_part_id__in=[planned_spare_part.spare_part.id]
        )

        in_stock = 0
        in_stock = balance_allocation(
            spare_parts_balances,
            in_stock,
            planned_spare_part,
        )

        similar_spare_parts_balances = StockBalance.objects.filter(
            spare_part_id__in=set(similar_spare_parts)
        )

        in_stock = balance_allocation(
            similar_spare_parts_balances, in_stock, planned_spare_part, is_similar=True
        )

        planned_spare_part.in_stock = in_stock
        planned_spare_part.save()


def balance_allocation(balances, in_stock, planned_spare_part, is_similar=False):
    original_spare_part_count = in_stock
    similar_parts_ids = {}
    for balance in balances:

        if balance.count == 0 or planned_spare_part.planned_count == in_stock:
            continue
        elif in_stock < planned_spare_part.planned_count:
            diff = planned_spare_part.planned_count - in_stock
            if diff > 0 and balance.count <= diff:
                in_stock += balance.count
                balance.count = 0
            else:
                left_in_stock_balance = balance.count - abs(
                    planned_spare_part.planned_count - in_stock
                )
                in_stock += abs(planned_spare_part.planned_count - in_stock)

                balance.count = left_in_stock_balance

        similar_parts_ids[balance.spare_part.id] = in_stock - original_spare_part_count
        balance.save()

    if is_similar:
        for id, value in similar_parts_ids.items():
            PlannedSparePart.objects.create(
                in_stock=value,
                spare_part_id=id,
                task_id=planned_spare_part.task.id,
                planned_count=0,
            )
        return original_spare_part_count

    return in_stock
