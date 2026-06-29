import json
import re

ORDERS = {
    "ORD-001": {
        "customer_name": "Ahmed Khan",
        "email": "ahmed.khan@gmail.com",
        "phone": "+92-300-1234567",
        "status": "Shipped",
        "item": "LaptopPro 15",
        "eta": "2024-12-20",
        "priority": "High",
        "payment_status": "Paid",
        "city": "Karachi"
    },
    "ORD-002": {
        "customer_name": "Hamza Khan",
        "email": "hamza.khan@gmail.com",
        "phone": "+92-300-12891567",
        "status": "Processing",
        "item": "SmartWatch X1",
        "eta": "2024-12-22",
        "priority": "Medium",
        "payment_status": "Paid",
        "city": "Lahore"
    },
    "ORD-003": {
        "customer_name": "Amna Khan",
        "email": "amna.khan@gmail.com",
        "phone": "+92-320-22374567",
        "status": "Delivered",
        "item": "Headphones Z",
        "eta": "Delivered",
        "priority": "Low",
        "payment_status": "Paid",
        "city": "Islamabad"
    },
    "ORD-004": {
        "customer_name": "Junaid Ansar",
        "email": "junaid.ali@gmail.com",
        "phone": "+92-300-1222567",
        "status": "Cancelled",
        "item": "Gaming Mouse GX",
        "eta": "Cancelled",
        "priority": "High",
        "payment_status": "Refunded",
        "city": "Karachi"
    },
    "ORD-005": {
        "customer_name": "Ayesha Jamshed",
        "email": "ayesha.umair@gmail.com",
        "phone": "+92-300-19814567",
        "status": "Returned",
        "item": "Bluetooth Speaker B2",
        "eta": "Returned",
        "priority": "Low",
        "payment_status": "Refunded",
        "city": "Faisalabad"
    },
}


def normalize_order_id(raw_id):
    digits = re.search(r'\d+', raw_id)
    if digits:
        number = digits.group().zfill(3)
        return f"ORD-{number}"
    return raw_id.strip().upper()


def format_order_as_text(order_id, order):
    return (
        f"Order ID: {order_id}. "
        f"Customer Name: {order['customer_name']}. "
        f"Email: {order['email']}. "
        f"Phone: {order['phone']}. "
        f"Status: {order['status']}. "
        f"Item: {order['item']}. "
        f"ETA: {order['eta']}. "
        f"Priority: {order['priority']}. "
        f"Payment Status: {order['payment_status']}. "
        f"City: {order['city']}."
    )


def lambda_handler(event, context):
    print("EVENT RECEIVED:")
    print(json.dumps(event, indent=2))

    action_group = event.get("actionGroup", "")
    function = event.get("function", "")

    params = {
        p.get("name"): p.get("value")
        for p in event.get("parameters", [])
        if "name" in p and "value" in p
    }

    print("Extracted Parameters:", params)

    if function == "get_order_status":
        order_id = params.get("orderId")

        if not order_id:
            response_text = "Error: Missing orderId parameter."
        else:
            order_id = normalize_order_id(order_id)
            print("Normalized Order ID:", order_id)
            order = ORDERS.get(order_id)
            if order:
                response_text = format_order_as_text(order_id, order)
            else:
                response_text = f"No order found with ID {order_id}."

    else:
        response_text = f"Error: Unknown function '{function}'."

    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "function": function,
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": response_text
                    }
                }
            }
        }
    }