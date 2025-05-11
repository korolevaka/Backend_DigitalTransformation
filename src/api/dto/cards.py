from pydantic import BaseModel, Field


class Case(BaseModel):
    required_it_points: int = Field(..., alias="requiredItPoints", description="Требования по IT очкам")
    required_hr_points: int = Field(..., alias="requiredHrPoints", description="Требования по HR очкам")
    required_ec_points: int = Field(..., alias="requiredEcPoints", description="Требования по EC очкам")
    required_bp_points: int = Field(..., alias="requiredBpPoints", description="Требования по BP очкам")


class Balance(BaseModel):
    dtc: int = Field(..., description="Нынешний баланс DTC")


class Score(BaseModel):
    total_it_points: int = Field(..., alias="totalItPoints", description="Количество IT очков")
    total_hr_points: int = Field(..., alias="totalHrPoints", description="Количество HR очков")
    total_ec_points: int = Field(..., alias="totalEcPoints", description="Количество EC очков")
    total_bp_points: int = Field(..., alias="totalBpPoints", description="Количество BP очков")


class Result(BaseModel):
    score: Score = Field(..., description="Счет")
    is_successful: bool = Field(..., alias="isSuccessful", description="Были ли достигнуты требования кейса")