"""Test the basic functionality of the package."""
from zhinst.timing_models import (
    PQSCMode,
    QAType,
    QCCSFeedbackModel,
    SGType,
    get_feedback_system_description,
)


def test_dummy_usage():
    description = get_feedback_system_description(
        generator_type=SGType.HDAWG,
        analyzer_type=QAType.SHFQA,
        pqsc_mode=PQSCMode.DECODER,
    )
    model = QCCSFeedbackModel(description=description)
    assert model.description == description

    latency = model.get_latency(10)
    assert isinstance(latency, int)
