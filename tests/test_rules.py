import pytest

from app.exceptions import BusinessRuleError, ConflictError
from app.models.reservation import Reservation
from app.services.rules import MaxDurationRule, NoOverlapRule, TimeOrderRule
from tests.conftest import dt


def make(start, end, status="active", id=1):
    return Reservation(id, 1, "Budi", start, end, status)


def test_time_order_rejects_end_before_start():
    with pytest.raises(BusinessRuleError):
        TimeOrderRule().validate(make(dt(10), dt(9)), [])


def test_time_order_rejects_same_time():
    with pytest.raises(BusinessRuleError):
        TimeOrderRule().validate(make(dt(10), dt(10)), [])


def test_max_duration_allows_exactly_3_hours():
    MaxDurationRule(3).validate(make(dt(9), dt(12)), [])


def test_max_duration_rejects_over_3_hours():
    with pytest.raises(BusinessRuleError):
        MaxDurationRule(3).validate(make(dt(9), dt(12, 1)), [])


def test_max_duration_is_configurable():
    with pytest.raises(BusinessRuleError):
        MaxDurationRule(1).validate(make(dt(9), dt(11)), [])


def test_no_overlap_rejects_overlapping_schedule():
    existing = [make(dt(9), dt(11))]
    with pytest.raises(ConflictError):
        NoOverlapRule().validate(make(dt(10), dt(12), id=2), existing)


def test_no_overlap_allows_back_to_back():
    existing = [make(dt(9), dt(10))]
    NoOverlapRule().validate(make(dt(10), dt(11), id=2), existing)


def test_no_overlap_ignores_cancelled_reservation():
    existing = [make(dt(9), dt(11), status="cancelled")]
    NoOverlapRule().validate(make(dt(10), dt(12), id=2), existing)
