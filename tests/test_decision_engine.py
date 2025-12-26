from app.services.decision_service import analyze_ticket_text

def test_high_confidence_payment_issue_is_p1():
    result = analyze_ticket_text(
        "My payment failed and this is unacceptable. Fix ASAP."
    )
    assert result["priority"] == "P1"
    assert result["confidence"] >= 0.75


def test_low_confidence_text_forces_safe_priority():
    result = analyze_ticket_text("Something strange happened")
    assert result["priority"] == "P2"  # forced safe default
    assert result["confidence"] < 0.75
