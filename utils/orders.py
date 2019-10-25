def calculateFurtherStatus(currentStatus):
    switcher = {
        "PENDING": [],
        "AWAITING_PAYMENT": [],
        "AWAITING_FULFIMENT": [
            "MANUAL_VERIFICATION_REQUIRED",
            "REFUNDED",
            "PARTIALLY_REFUNDED",
            "AWAITING_SHIPMENT"
        ],
        "AWAITING_SHIPMENT": [
            "SHIPPED",
            "PARTIALLY_SHIPPED",
            "AWAITING_PICKUP",
        ],
        "SHIPPED": ["COMPLETED"],
        "PARTIALLY_SHIPPED": ["COMPLETED"],
        "AWAITING_PICKUP": ["COMPLETED"],
        "MANUAL_VERIFICATION_REQUIRED": ["AWAITING_FULFIMENT"]
    }
    return switcher.get(currentStatus, [])