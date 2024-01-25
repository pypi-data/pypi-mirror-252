import os
import threading
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import datajoint as dj
from ..models.LabMember import LabMember, GetLabMembersResponse
from ..models.Session import Session, GetSessionsResponse
from ..models.IntervalList import IntervalList, GetIntervalListsResponse
from ..models.Subject import Subject, GetSubjectsResponse

app = FastAPI()

origins = [
    'http://localhost:3000',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)

spyglass_config_path = os.environ.get("SPYGLASS_CONFIG_PATH", None)
if spyglass_config_path is None:
    raise Exception("Please set SPYGLASS_CONFIG_PATH environment variable")
dj.config.load(spyglass_config_path)

import spyglass.common as sgc  # noqa: E402
# from spyglass.common.common_lab import decompose_name  # noqa: E402
# from spyglass.utils.nwb_helper_fn import get_nwb_copy_filename  # noqa: E402

##############################################################################
# not exactly sure why this is needed.
# but if I don't use it I get "Packet sequence number wrong" error serving responses simultaneously
# and that seems to be a datajoint/mysql issue
lock = threading.Lock()


@app.get("/api/v1/probe")
def probe():
    return {"Hello": "World"}


# @app.post("/api/v1/common/lab-members")
# def add_lab_member(data: AddLabMemberRequest):
#     # we don't use the LabMember.insert_from_name method because we want to raise an error if the name already exists
#     _, first, last = decompose_name(data.full_name)
#     try:
#         sgc.LabMember.insert1(
#             dict(
#                 lab_member_name=f"{first} {last}",
#                 first_name=first,
#                 last_name=last,
#             ),
#             skip_duplicates=False,
#         )
#     except dj.errors.DuplicateError:
#         raise HTTPException(status_code=400, detail="Lab member already exists")
#     return {"success": True}


@app.get("/api/v1/common/lab-members")
def lab_members(limit: Optional[int] = 10, offset: Optional[int] = 0):
    with lock:
        if limit > 200:
            raise HTTPException(status_code=400, detail="Limit must be <= 200")
        x = sgc.LabMember.fetch(as_dict=True, limit=limit, offset=offset)
        return GetLabMembersResponse(lab_members=[
            LabMember.from_dict(a) for a in x
        ])


# @app.post("/api/v1/common/sessions")
# def add_session(data: AddSessionRequest):
#     # data.nwb_file_name needs to be in the spyglass raw directory
#     copy_nwb_file_name = get_nwb_copy_filename(data.nwb_file_name)
#     if len(Nwbfile() & {"nwb_file_name": copy_nwb_file_name}):
#         raise HTTPException(status_code=400, detail="Session already exists")
#     insert_sessions(data.nwb_file_name)
#     return {"success": True}


@app.get("/api/v1/common/sessions")
def get_sessions(limit: Optional[int] = 10, offset: Optional[int] = 0, subject_id: Optional[str] = None, nwb_file_name: Optional[str] = None):
    with lock:
        if limit > 200:
            raise HTTPException(status_code=400, detail="Limit must be <= 200")
        key = {}
        if subject_id is not None:
            key["subject_id"] = subject_id
        if nwb_file_name is not None:
            key["nwb_file_name"] = nwb_file_name
        x = (sgc.Session & key).fetch(as_dict=True, limit=limit, offset=offset)
        return GetSessionsResponse(sessions=[
            Session.from_dict(a)
            for a in x
        ])


# def get_original_nwb_filename(copy_nwb_file_name):
#     """Get original file name of copy of nwb file"""

#     filename, file_extension = os.path.splitext(copy_nwb_file_name)

#     if not filename.endswith("_"):
#         return copy_nwb_file_name

#     return f"{filename[:-1]}{file_extension}"


@app.get("/api/v1/common/interval-lists")
def get_interval_lists(limit: Optional[int] = 10, offset: Optional[int] = 0):
    with lock:
        if limit > 200:
            raise HTTPException(status_code=400, detail="Limit must be <= 200")
        x = sgc.IntervalList().fetch(as_dict=True, limit=limit, offset=offset)
        return GetIntervalListsResponse(interval_lists=[
            IntervalList.from_dict(a) for a in x
        ])


@app.get("/api/v1/common/subjects")
def get_subjects(limit: Optional[int] = 10, offset: Optional[int] = 0):
    with lock:
        if limit > 200:
            raise HTTPException(status_code=400, detail="Limit must be <= 200")
        x = sgc.Subject().fetch(as_dict=True, limit=limit, offset=offset)
        return GetSubjectsResponse(subjects=[
            Subject.from_dict(a) for a in x
        ])
