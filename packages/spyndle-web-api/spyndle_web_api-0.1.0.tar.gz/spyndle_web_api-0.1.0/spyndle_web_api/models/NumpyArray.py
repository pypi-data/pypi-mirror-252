from typing import List
import base64
import numpy as np
from pydantic import BaseModel


class NumpyArray(BaseModel):
    dtype: str
    shape: List[int]
    data_base64: str

    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        return cls(
            dtype=str(arr.dtype),
            shape=list(arr.shape),
            data_base64=base64.b64encode(arr.tobytes()).decode('utf-8')
        )

    def to_numpy(self):
        return np.frombuffer(base64.b64decode(self.data_base64), dtype=self.dtype).reshape(self.shape)
