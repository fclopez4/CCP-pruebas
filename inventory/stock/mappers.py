from . import models, schemas


def delivery_to_schema(
    purchase: models.Delivery,
) -> schemas.DeliveryDetailSchema:
    return schemas.DeliveryDetailSchema(
        id=purchase.id,
        purchase_id=purchase.purchase_id,
        address_id=purchase.address_id,
        user_id=purchase.user_id,
        status=purchase.status,
        created_at=purchase.created_at,
        updated_at=purchase.updated_at,
        delivery_date=purchase.delivery_date,
        items=[
            schemas.DeliveryItemResponseSchema(
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in purchase.items
        ],
    )


def stock_list_to_schema(stock_list: list[models.Stock]) -> list[schemas.StockResponseSchema]:
    return [
        schemas.StockResponseSchema(
            product_id=stock.product_id,
            warehouse_id=stock.warehouse_id,
            quantity=stock.quantity,
            last_updated= stock.updated_at or stock.created_at
        )
        for stock in stock_list
    ]