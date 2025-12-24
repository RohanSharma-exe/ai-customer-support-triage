def generate_reply(intent: str, sentiment: str, urgency: str, order_id: str | None) -> dict:
    # Base templates (policy-safe)
    templates = {
        "PAYMENT_ISSUE": (
            "We’re sorry for the trouble with your payment{order_ref}. "
            "Our team is reviewing this and will update you shortly."
        ),
        "ORDER_DELAY": (
            "We apologize for the delay{order_ref}. "
            "We’re checking the shipment status and will share an update soon."
        ),
        "REFUND_RETURN": (
            "We understand your request regarding a refund or return{order_ref}. "
            "We’re reviewing the details and will assist you as per policy."
        ),
        "DAMAGED_PRODUCT": (
            "Sorry to hear about the condition of the product{order_ref}. "
            "We’ll help resolve this as quickly as possible."
        ),
        "WRONG_ITEM": (
            "Apologies for the incorrect item{order_ref}. "
            "We’re checking the order details and next steps."
        ),
        "ACCOUNT_ISSUE": (
            "We’re here to help with your account issue. "
            "Please allow us a moment to review your details."
        ),
        "DEFAULT": (
            "Thank you for reaching out. "
            "We’re reviewing your request and will get back to you shortly."
        ),
    }

    order_ref = f" for order {order_id}" if order_id else ""
    base = templates.get(intent, templates["DEFAULT"]).format(order_ref=order_ref)

    # Tone adjustments
    if sentiment == "NEGATIVE":
        base = "We’re sorry for the inconvenience. " + base

    if urgency == "HIGH":
        base += " We understand the urgency and are prioritizing this."

    return {
        "draft_reply": base,
        "confidence": 0.75,
        "explanation": f"Template={intent}, Sentiment={sentiment}, Urgency={urgency}"
    }
