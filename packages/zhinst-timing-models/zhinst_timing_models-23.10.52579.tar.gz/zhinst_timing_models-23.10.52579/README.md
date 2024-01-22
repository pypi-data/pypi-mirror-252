# Feedback Latency Model Parameters

[![PyPI - Version](https://img.shields.io/pypi/v/zhinst-timing-models.svg)](https://pypi.org/project/zhinst-timing-models)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zhinst-timing-models.svg)](https://pypi.org/project/zhinst-timing-models)

-----

Feedback Data Latency model for PQSC, SHF- and HDAWG systems.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install zhinst-timing-models
```

## Usage

```python
from zhinst.timing_models import (
    PQSCMode,
    QAType,
    QCCSFeedbackModel,
    SGType,
    get_feedback_system_description,
)

model = QCCSFeedbackModel(
    description=get_feedback_system_description(
        generator_type=SGType.HDAWG,
        analyzer_type=QAType.SHFQA,
        pqsc_mode=PQSCMode.DECODER,
        )
    )
awg_clock_cycles = model.get_latency(...)
```

## License

`zhinst-timing-models` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
