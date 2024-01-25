from typing import List
from pydantic import BaseModel
from .NumpyArray import NumpyArray


class IntervalList(BaseModel):
    interval_list_name: str
    valid_times: NumpyArray
    pipeline: str
    nwb_file_name: str

    @classmethod
    def from_dict(cls, a: dict):
        return cls(
            interval_list_name=a["interval_list_name"],
            valid_times=NumpyArray.from_numpy(a["valid_times"]),
            pipeline=a["pipeline"],
            nwb_file_name=a['nwb_file_name']
        )


class GetIntervalListsResponse(BaseModel):
    interval_lists: List[IntervalList]
