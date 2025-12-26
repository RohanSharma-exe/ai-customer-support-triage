from datetime import datetime, timedelta, timezone

def test_resolution_time_calculation():
    created_at = datetime.now(timezone.utc) - timedelta(minutes=30)
    resolved_at = datetime.now(timezone.utc)

    resolution_delta = resolved_at - created_at
    resolution_time_hours = resolution_delta.total_seconds() / 3600

    assert round(resolution_time_hours, 2) == 0.5
