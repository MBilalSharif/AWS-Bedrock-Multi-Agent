import json
import re

RETURNS = {
    "ORD-001": {
        "customer_name": "Ahmed Khan",
        "email": "ahmed.khan@gmail.com",
        "phone": "+92-300-1234567",
        "item": "LaptopPro 15",
        "eligible": False,
        "reason": "Order is shipped and in transit, not yet delivered",
        "refund_status": "Not Applicable",
        "city": "Karachi"
    },
    "ORD-002": {
        "customer_name": "Hamza Khan",
        "email": "hamza.khan@gmail.com",
        "phone": "+92-300-12891567",
        "item": "SmartWatch X1",
        "eligible": False,
        "reason": "Order is still processing, cannot initiate return yet",
        "refund_status": "Not Applicable",
        "city": "Lahore"
    },
    "ORD-003": {
        "customer_name": "Amna Khan",
        "email": "amna.khan@gmail.com",
        "phone": "+92-320-22374567",
        "item": "Headphones Z",
        "eligible": True,
        "reason": "Delivered and within 30-day return window",
        "refund_status": "Pending Initiation",
        "city": "Islamabad"
    },
    "ORD-004": {
        "customer_name": "Junaid Ansar",
        "email": "junaid.ali@gmail.com",
        "phone": "+92-300-1222567",
        "item": "Gaming Mouse GX",
        "eligible": False,
        "reason": "Cancelled orders are not eligible for return",
        "refund_status": "Already Refunded",
        "city": "Karachi"
    },
    "ORD-005": {
        "customer_name": "Ayesha Jamshed",
        "email": "ayesha.umair@gmail.com",
        "phone": "+92-300-19814567",
        "item": "Bluetooth Speaker B2",
        "eligible": True,
        "reason": "Return already initiated within policy window",
        "refund_status": "Refunded",
        "city": "Faisalabad"
    },
}


def normalize_order_id(raw_id):
    digits = re.search(r'\d+', raw_id)
    if digits:
        number = digits.group().zfill(3)
        return f"ORD-{number}"
    return raw_id.strip().upper()


def format_return_as_text(order_id, data):
    eligible_text = "eligible" if data["eligible"] else "not eligible"
    return (
        f"Order ID: {order_id}. "
        f"Customer Name: {data['customer_name']}. "
        f"Email: {data['email']}. "
        f"Phone: {data['phone']}. "
        f"Item: {data['item']}. "
        f"Return Eligibility: {eligible_text}. "
        f"Reason: {data['reason']}. "
        f"Refund Status: {data['refund_status']}. "
        f"City: {data['city']}."
    )


def lambda_handler(event, context):
    print("EVENT RECEIVED:", json.dumps(event))

    action_group = event.get("actionGroup", "")
    function = event.get("function", "")

    params = {
        p.get("name"): p.get("value")
        for p in event.get("parameters", [])
        if "name" in p and "value" in p
    }

    if function == "get_return_status":
        order_id = params.get("order_id")

        if not order_id:
            response_text = "Error: Missing order_id parameter."
        else:
            order_id = normalize_order_id(order_id)
            print("Normalized Order ID:", order_id)
            data = RETURNS.get(order_id)
            if data:
                response_text = format_return_as_text(order_id, data)
            else:
                response_text = f"No return information found for order ID {order_id}."
    else:
        response_text = f"Error: Unknown function {function}."

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