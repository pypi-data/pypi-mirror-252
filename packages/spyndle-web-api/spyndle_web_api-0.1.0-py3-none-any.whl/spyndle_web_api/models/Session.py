from typing import List
from datetime import datetime
from pydantic import BaseModel


class Session(BaseModel):
    nwb_file_name: str
    subject_id: str
    institution_name: str
    lab_name: str
    session_id: str
    session_description: str
    session_start_time: datetime
    timestamps_reference_time: datetime
    experiment_description: str

    @classmethod
    def from_dict(cls, a: dict):
        return cls(
            nwb_file_name=a["nwb_file_name"],
            subject_id=a["subject_id"],
            institution_name=a["institution_name"],
            lab_name=a["lab_name"],
            session_id=a["session_id"],
            session_description=a["session_description"],
            session_start_time=a["session_start_time"],
            timestamps_reference_time=a["timestamps_reference_time"],
            experiment_description=a["experiment_description"],
        )


# class AddSessionRequest(BaseModel):
#     nwb_file_name: str


class GetSessionsResponse(BaseModel):
    sessions: List[Session]
