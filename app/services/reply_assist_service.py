from app.ai.reply_generator import generate_reply

def create_reply_draft(intent: str, sentiment: str, urgency: str, order_id: str | None) -> dict:
    return generate_reply(
        intent=intent,
        sentiment=sentiment,
        urgency=urgency,
        order_id=order_id
    )
