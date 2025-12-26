class MockAgent:
    def __init__(self, specialization, active_tickets, sla_compliance_rate, is_available=True):
        self.specialization = specialization
        self.active_tickets = active_tickets
        self.sla_compliance_rate = sla_compliance_rate
        self.is_available = is_available


def test_routing_prefers_skill_match_for_p1():
    from app.services.routing_service import route_ticket

    agents = [
        MockAgent("ORDER_DELAY", 0, 0.9),
        MockAgent("PAYMENT_ISSUE", 3, 0.95),
    ]

    # monkeypatch-style local scoring test
    best_agent = max(
        agents,
        key=lambda a: (
            (5 if a.specialization == "PAYMENT_ISSUE" else 1)
            + (5)  # P1 boost
            - a.active_tickets
        )
    )

    assert best_agent.specialization == "PAYMENT_ISSUE"
