from typing import List
from pydantic import BaseModel


class Subject(BaseModel):
    subject_id: str
    description: str
    genotype: str
    sex: str
    species: str

    @classmethod
    def from_dict(cls, a: dict):
        return cls(
            subject_id=a['subject_id'],
            description=a.get('description', '') or '',
            genotype=a.get('genotype', '') or '',
            sex=a.get('sex', '') or '',
            species=a.get('species', '') or ''
        )


class GetSubjectsResponse(BaseModel):
    subjects: List[Subject]
