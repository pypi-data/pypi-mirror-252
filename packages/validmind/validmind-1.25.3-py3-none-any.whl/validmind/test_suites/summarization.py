# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Test suites for llm summarization models
"""

from validmind.vm_models import TestSuite


class SummarizationMetrics(TestSuite):
    """
    Test suite for Summarization metrics
    """

    suite_id = "summarization_metrics"
    tests = [
        "validmind.model_validation.RougeMetrics",
        "validmind.model_validation.TokenDisparity",
        "validmind.model_validation.BleuScore",
        "validmind.model_validation.BertScore",
        "validmind.model_validation.ContextualRecall",
    ]
