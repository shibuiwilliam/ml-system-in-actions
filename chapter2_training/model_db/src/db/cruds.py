import uuid
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from src.db import models, schemas


def select_project_all(db: Session) -> List[schemas.Project]:
    return db.query(models.Project).all()


def select_project_by_id(
    db: Session,
    project_id: str,
) -> schemas.Project:
    return db.query(models.Project).filter(models.Project.project_id == project_id).first()


def select_project_by_name(
    db: Session,
    project_name: str,
) -> schemas.Project:
    return db.query(models.Project).filter(models.Project.project_name == project_name).first()


def add_project(
    db: Session,
    project_name: str,
    description: Optional[str] = None,
    commit: bool = True,
) -> schemas.Project:
    exists = select_project_by_name(
        db=db,
        project_name=project_name,
    )
    if exists:
        return exists
    else:
        project_id = str(uuid.uuid4())[:6]
        data = models.Project(
            project_id=project_id,
            project_name=project_name,
            description=description,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
        return data


def select_model_all(db: Session) -> List[schemas.Model]:
    return db.query(models.Model).all()


def select_model_by_id(
    db: Session,
    model_id: str,
) -> schemas.Model:
    return db.query(models.Model).filter(models.Model.model_id == model_id).first()


def select_model_by_project_id(
    db: Session,
    project_id: str,
) -> List[schemas.Model]:
    return db.query(models.Model).filter(models.Model.project_id == project_id).all()


def select_model_by_project_name(
    db: Session,
    project_name: str,
) -> List[schemas.Model]:
    project = select_project_by_name(
        db=db,
        project_name=project_name,
    )
    return db.query(models.Model).filter(models.Model.project_id == project.project_id).all()


def select_model_by_name(
    db: Session,
    model_name: str,
) -> List[schemas.Model]:
    return db.query(models.Model).filter(models.Model.model_name == model_name).all()


def add_model(
    db: Session,
    project_id: str,
    model_name: str,
    description: Optional[str] = None,
    commit: bool = True,
) -> schemas.Model:
    models_in_project = select_model_by_project_id(
        db=db,
        project_id=project_id,
    )
    for model in models_in_project:
        if model.model_name == model_name:
            return model
    model_id = str(uuid.uuid4())[:6]
    data = models.Model(
        model_id=model_id,
        project_id=project_id,
        model_name=model_name,
        description=description,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


def select_experiment_all(db: Session) -> List[schemas.Experiment]:
    return db.query(models.Experiment).all()


def select_experiment_by_id(
    db: Session,
    experiment_id: str,
) -> schemas.Experiment:
    return db.query(models.Experiment).filter(models.Experiment.experiment_id == experiment_id).first()


def select_experiment_by_model_version_id(
    db: Session,
    model_version_id: str,
) -> schemas.Experiment:
    return db.query(models.Experiment).filter(models.Experiment.model_version_id == model_version_id).first()


def select_experiment_by_model_id(
    db: Session,
    model_id: str,
) -> List[schemas.Experiment]:
    return db.query(models.Experiment).filter(models.Experiment.model_id == model_id).all()


def select_experiment_by_project_id(
    db: Session,
    project_id: str,
) -> List[schemas.Experiment]:
    return (
        db.query(models.Experiment, models.Model)
        .filter(models.Model.project_id == project_id)
        .filter(models.Experiment.model_id == models.Model.model_id)
        .all()
    )


def add_experiment(
    db: Session,
    model_version_id: str,
    model_id: str,
    parameters: Optional[Dict] = None,
    training_dataset: Optional[str] = None,
    validation_dataset: Optional[str] = None,
    test_dataset: Optional[str] = None,
    evaluations: Optional[Dict] = None,
    artifact_file_paths: Optional[Dict] = None,
    commit: bool = True,
) -> schemas.Experiment:
    experiment_id = str(uuid.uuid4())[:6]
    data = models.Experiment(
        experiment_id=experiment_id,
        model_version_id=model_version_id,
        model_id=model_id,
        parameters=parameters,
        training_dataset=training_dataset,
        validation_dataset=validation_dataset,
        test_dataset=test_dataset,
        evaluations=evaluations,
        artifact_file_paths=artifact_file_paths,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


def update_experiment_evaluation(
    db: Session,
    experiment_id: str,
    evaluations: Dict,
) -> schemas.Experiment:
    data = select_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )
    if data.evaluations is None:
        data.evaluations = evaluations
    else:
        for k, v in evaluations.items():
            data.evaluations[k] = v
    db.commit()
    db.refresh(data)
    return data


def update_experiment_artifact_file_paths(
    db: Session,
    experiment_id: str,
    artifact_file_paths: Dict,
) -> schemas.Experiment:
    data = select_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )
    if data.artifact_file_paths is None:
        data.artifact_file_paths = artifact_file_paths
    else:
        for k, v in artifact_file_paths.items():
            data.artifact_file_paths[k] = v
    db.commit()
    db.refresh(data)
    return data
