from pydantic import BaseModel


class Case(BaseModel):
    required_it_points: int
    required_hr_points: int
    required_ec_points: int
    required_bp_points: int


class Balance(BaseModel):
    dtc: int


class Score(BaseModel):
    total_it_points: int
    total_hr_points: int
    total_ec_points: int
    total_bp_points: int


class Result(BaseModel):
    score: Score
    is_successful: bool