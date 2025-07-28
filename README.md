# Body Composition Checkup


*Author*: Luca Zoffoli, Ph.D.

---

## 📦 Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## 🧠 Modules Overview

### `onnx_models.py`

Defines the `OnnxModel` class, a wrapper around ONNX models using `onnxruntime`.

**Key Features:**
- Accepts input as `np.ndarray`, `pd.DataFrame`, or `dict`
- Validates input shape and labels
- Returns predictions in the same format as input
- Supports flexible integration with other systems

---

### `checkupy.py`

Implements a full BIA analysis pipeline with multiple methodologies.

#### Core Classes

- **`BIAInput`**: Base class for managing anthropometric and electrical data.
  - Orthostatic correction methods
  - Validation of electrical measurements
  - Computation of impedance and phase angles

- **`Fitness`**: Extends `BIAInput` with custom equations for:
  - Water content
  - Fat-free mass
  - Fat mass
  - Bone mineral content
  - Skeletal muscle mass
  - Basal metabolic rate

- **`Standard`**: Extends `Fitness` using literature-based equations and applies orthostatic corrections.

- **`Inbody`**: Uses a pre-trained ONNX model (`model2_100x2_vs_inbody.onnx`) to predict body composition metrics. It maps input features and output labels to the model using `OnnxModel`.

- **`CheckupBIA`**: Aggregates all three approaches (`Fitness`, `Standard`, `Inbody`) into a unified interface.

## 🧬 ONNX Model Integration

The `Inbody` class uses a pre-trained ONNX model (`model2_100x2_vs_inbody.onnx`) to estimate body composition metrics. This model is loaded via the `OnnxModel` class and expects a specific order of input features. Predictions are returned as a dictionary of labeled outputs.

This approach allows for fast, scalable, and consistent inference across platforms, leveraging the power of machine learning while maintaining compatibility with traditional BIA inputs.


## 🚀 Example Usage

### Manual input of all data

```python
from checkupy import CheckupBIA
import pandas as pd

# create the checkup measurement object
checkup = CheckupBIA(
    height=175,
    weight=70,
    age=30,
    gender="M",
    left_arm_resistance=320,
    left_arm_reactance=45,
    left_trunk_resistance=300,
    left_trunk_reactance=40,
    left_leg_resistance=280,
    left_leg_reactance=35,
    left_body_resistance=290,
    left_body_reactance=38,
    right_arm_resistance=325,
    right_arm_reactance=46,
    right_trunk_resistance=305,
    right_trunk_reactance=41,
    right_leg_resistance=285,
    right_leg_reactance=36,
    right_body_resistance=295,
    right_body_reactance=39,
)

# print all results
results = []
for equation, data in checkup.to_dict().items():
    line = pd.DataFrame(pd.Series(data)).T
    line.index = pd.Index([equation])
    results += [line]
print(pd.concat(results).T)
```

### Automatic reading from *json* file

```python
from checkupy import CheckupBIA
import pandas as pd
import json

# here we load all the required data from a json file.
# It must have the same key-value structure of the
# example above
with open("bia_sample.json", "r") as f:
    params = json.load(f)
    bia = CheckupBIA(**params)
    out = []
    for i, v in bia.to_dict().items():
        line = pd.DataFrame(pd.Series(v)).T
        line.index = pd.Index([i])
        out.append(line)
out = pd.concat(out).T

# we print the results
print("\nBIA Results:\n")
print(out.to_string(index=True))

# we save them as csv file for later use
out.to_csv("checkupy_results.csv")
```

### Using the console


```bash
python run.py --json bia_axample.json --output "bia_results.csv"
```
