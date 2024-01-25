from typing import List

from ..models.LabMember import GetLabMembersResponse, LabMember
from ..models.Session import GetSessionsResponse
from ..models.IntervalList import GetIntervalListsResponse
from ..models.Subject import GetSubjectsResponse
import requests


class Client:
    def __init__(self):
        self._api_base_url = "http://localhost:5023/api/v1"

    def probe(self):
        url = self._api_base_url + "/probe"
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(f"Error: {r.status_code}: {r.text}")
        return r.json()

    def check1(self):
        url = self._api_base_url + "/check1"
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(f"Error: {r.status_code}: {r.text}")
        return r.json()

    # def add_lab_member(self, full_name):
    #     url = self._api_base_url + "/common/lab-members"
    #     req = AddLabMemberRequest(full_name=full_name)
    #     r = requests.post(url, json=req.model_dump())
    #     if r.status_code != 200:
    #         raise Exception(f"Error: {r.status_code}: {r.text}")
    #     resp = r.json()
    #     if not resp["success"]:
    #         raise Exception(f"Unexpected response: {resp}")

    def get_lab_members(self) -> List[LabMember]:
        limit = 20
        offset = 0
        while True:
            url = (
                self._api_base_url
                + f"/common/lab-members?limit={limit}&offset={offset}"
            )
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception(f"Error: {r.status_code}: {r.text}")
            resp = GetLabMembersResponse(**r.json())
            if len(resp.lab_members) == 0:
                break
            for m in resp.lab_members:
                yield m
            offset += limit

    # def add_session(self, nwb_fname):
    #     url = self._api_base_url + "/common/sessions"
    #     req = AddSessionRequest(nwb_file_name=nwb_fname)
    #     r = requests.post(url, json=req.model_dump())
    #     if r.status_code != 200:
    #         raise Exception(f"Error: {r.status_code}: {r.text}")
    #     resp = r.json()
    #     if not resp["success"]:
    #         raise Exception(f"Unexpected response: {resp}")

    def get_sessions(self):
        limit = 20
        offset = 0
        while True:
            url = self._api_base_url + f"/common/sessions?limit={limit}&offset={offset}"
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception(f"Error: {r.status_code}: {r.text}")
            resp = GetSessionsResponse(**r.json())
            if len(resp.sessions) == 0:
                break
            for s in resp.sessions:
                yield s
            offset += limit

    def get_interval_lists(self):
        limit = 20
        offset = 0
        while True:
            url = (
                self._api_base_url
                + f"/common/interval-lists?limit={limit}&offset={offset}"
            )
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception(f"Error: {r.status_code}: {r.text}")
            resp = GetIntervalListsResponse(**r.json())
            if len(resp.interval_lists) == 0:
                break
            for il in resp.interval_lists:
                yield il
            offset += limit

    def get_subjects(self):
        limit = 20
        offset = 0
        while True:
            url = self._api_base_url + f"/common/subjects?limit={limit}&offset={offset}"
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception(f"Error: {r.status_code}: {r.text}")
            resp = GetSubjectsResponse(**r.json())
            if len(resp.subjects) == 0:
                break
            for s in resp.subjects:
                yield s
            offset += limit
