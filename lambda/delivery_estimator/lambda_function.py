from decimal import Decimal, InvalidOperation


def lambda_handler(event, context):
    try:
        items = event["items"]

        if not isinstance(items, list) or not items:
            raise ValueError("items must be a non-empty list")

        subtotal = Decimal("0.00")

        for item in items:
            price = Decimal(str(item["price"]))
            quantity = item["quantity"]

            if not price.is_finite() or price < 0:
                raise ValueError("price must be a non-negative number")

            if type(quantity) is not int or quantity < 1:
                raise ValueError("quantity must be a positive integer")

            subtotal += price * quantity

        subtotal = subtotal.quantize(Decimal("0.01"))

        delivery_fee = (
            Decimal("0.00")
            if subtotal >= Decimal("50.00")
            else Decimal("4.99")
        )

        total = subtotal + delivery_fee

        return {
            "statusCode": 200,
            "body": {
                "subtotal": str(subtotal),
                "delivery_fee": str(delivery_fee),
                "total": str(total),
                "currency": "EUR"
            }
        }

    except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
        return {
            "statusCode": 400,
            "body": {
                "error": str(exc)
            }
        }
