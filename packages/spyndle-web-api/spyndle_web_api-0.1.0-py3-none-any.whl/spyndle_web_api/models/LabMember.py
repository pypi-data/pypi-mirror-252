from typing import List
from pydantic import BaseModel, Field


class LabMember(BaseModel):
    lab_member_name: str = Field(..., description="Full name of the lab member")
    first_name: str = Field(..., description="First name of the lab member")
    last_name: str = Field(..., description="Last name of the lab member")

    @classmethod
    def from_dict(cls, a: dict):
        return LabMember(
            lab_member_name=a["lab_member_name"],
            first_name=a["first_name"],
            last_name=a["last_name"]
        )


# Get lab members
class GetLabMembersResponse(BaseModel):
    lab_members: List[LabMember]


# # Add lab member
# class AddLabMemberRequest(BaseModel):
#     full_name: str
