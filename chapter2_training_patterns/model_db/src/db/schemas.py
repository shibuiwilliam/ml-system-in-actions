from typing import Optional, Dict
import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    project_name: str
    description: Optional[str]


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    project_id: int
    created_datetime: datetime.datetime

    class Config:
        orm_mode = True


class ModelBase(BaseModel):
    project_id: str
    model_name: str
    description: Optional[str]


class ModelCreate(ModelBase):
    pass


class Model(ModelBase):
    model_id: int
    created_datetime: datetime.datetime

    class Config:
        orm_mode = True


class ExperimentBase(BaseModel):
    model_id: str
    parameters: Optional[Dict]
    training_dataset: Optional[str]
    validation_dataset: Optional[str]
    test_dataset: Optional[str]
    evaluations: Optional[Dict]
    model_file_path: Optional[str]


class ExperimentCreate(ExperimentBase):
    pass


class Experiment(ExperimentBase):
    experiment_id: int
    created_datetime: datetime.datetime

    class Config:
        orm_mode = True
