"""
module allowing to use onnx models
"""

#! IMPORTS


import numpy as np
import onnx
import pandas as pd
from onnxruntime import InferenceSession

#! CLASSES


class OnnxModel:
    def __init__(
        self,
        model_path: str,
        input_labels: list[str],
        output_labels: list[str],
    ):
        self.model_path = model_path
        self._input_labels = input_labels
        self._output_labels = output_labels
        self.session = InferenceSession(model_path)
        self.model = onnx.load(model_path)

    @property
    def input_labels(self):
        return self._input_labels

    @property
    def output_labels(self):
        return self._output_labels

    def predict(self, data):

        # check the inputs
        target_cols = len(self._input_labels)
        wrong_cols = f"Expected input tensor with shape (N, {target_cols})"
        col_list = f"DataFrame must contain columns: {self._input_labels}"

        if isinstance(data, np.ndarray):
            if data.ndim != 2 or data.shape[1] != target_cols:
                raise ValueError(wrong_cols)
            vals = data.astype(np.float32)
            source = "ndarray"

        elif isinstance(data, pd.DataFrame):
            if not all(label in data.columns for label in self._input_labels):
                raise ValueError(col_list)
            vals = data[self._input_labels].values.astype(np.float32)
            source = "dataframe"

        elif isinstance(data, dict):
            if not all(label in data.keys() for label in self._input_labels):
                raise ValueError(col_list)
            vals = []
            for i in self._input_labels:
                if isinstance(data[i], (pd.DataFrame, pd.Series)):
                    vals.append(data[i].values.astype(np.float32).flatten())
                else:
                    vals.append(data[i].astype(np.float32).flatten())
            vals = np.concatenate([i.reshape(-1, 1) for i in vals], axis=1)
            source = "dict"

        else:
            raise TypeError("Unsupported input type")

        # make the inference
        inputs = {self.session.get_inputs()[0].name: vals}
        outputs = self.session.run(None, inputs)[0]

        # adjust the outputs
        if source == "ndarray":
            return outputs

        if source == "dict":
            return {
                i: v.astype(np.float32).flatten()
                for i, v in zip(self.output_labels, outputs.T)  # type: ignore
            }

        if source == "dataframe":
            return pd.DataFrame(
                data=outputs,  # type: ignore
                index=data.index,  # type: ignore
                columns=self.output_labels,
            )

        raise TypeError("Unsupported output type")

    def __call__(self, data):
        return self.predict(data)
