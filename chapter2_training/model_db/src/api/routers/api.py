from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db import cruds, schemas
from src.db.database import get_db

router = APIRouter()


@router.get("/projects/all")
def project_all(db: Session = Depends(get_db)):
    return cruds.select_project_all(db=db)


@router.get("/projects/id/{project_id}")
def project_by_id(
    project_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_project_by_id(
        db=db,
        project_id=project_id,
    )


@router.get("/projects/name/{project_name}")
def project_by_name(
    project_name: str,
    db: Session = Depends(get_db),
):
    return cruds.select_project_by_name(
        db=db,
        project_name=project_name,
    )


@router.post("/projects")
def add_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    return cruds.add_project(
        db=db,
        project_name=project.project_name,
        description=project.description,
        commit=True,
    )


@router.get("/models/all")
def model_all(db: Session = Depends(get_db)):
    return cruds.select_model_all(db=db)


@router.get("/models/id/{model_id}")
def model_by_id(
    model_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_model_by_id(
        db=db,
        model_id=model_id,
    )


@router.get("/models/project-id/{project_id}")
def model_by_project_id(
    project_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_model_by_project_id(
        db=db,
        project_id=project_id,
    )


@router.get("/models/name/{model_name}")
def model_by_name(
    model_name: str,
    db: Session = Depends(get_db),
):
    return cruds.select_model_by_name(
        db=db,
        model_name=model_name,
    )


@router.get("/models/project-name/{model_name}")
def model_by_project_name(
    project_name: str,
    db: Session = Depends(get_db),
):
    return cruds.select_model_by_project_name(
        db=db,
        project_name=project_name,
    )


@router.post("/models")
def add_model(
    model: schemas.ModelCreate,
    db: Session = Depends(get_db),
):
    return cruds.add_model(
        db=db,
        project_id=model.project_id,
        model_name=model.model_name,
        description=model.description,
        commit=True,
    )


@router.get("/experiments/all")
def experiment_all(db: Session = Depends(get_db)):
    return cruds.select_experiment_all(db=db)


@router.get("/experiments/id/{experiment_id}")
def experiment_by_id(
    experiment_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )


@router.get("/experiments/model-version-id/{model_version_id}")
def experiment_by_model_version_id(
    model_version_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_experiment_by_model_version_id(
        db=db,
        model_version_id=model_version_id,
    )


@router.get("/experiments/model-id/{model_id}")
def experiment_by_model_id(
    model_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_experiment_by_model_id(
        db=db,
        model_id=model_id,
    )


@router.get("/experiments/project-id/{project_id}")
def experiment_by_project_id(
    project_id: str,
    db: Session = Depends(get_db),
):
    return cruds.select_experiment_by_project_id(
        db=db,
        project_id=project_id,
    )


@router.post("/experiments")
def add_experiment(
    experiment: schemas.ExperimentCreate,
    db: Session = Depends(get_db),
):
    return cruds.add_experiment(
        db=db,
        model_version_id=experiment.model_version_id,
        model_id=experiment.model_id,
        parameters=experiment.parameters,
        training_dataset=experiment.training_dataset,
        validation_dataset=experiment.validation_dataset,
        test_dataset=experiment.test_dataset,
        evaluations=experiment.evaluations,
        artifact_file_paths=experiment.artifact_file_paths,
        commit=True,
    )


@router.post("/experiments/evaluations/{experiment_id}")
def update_evaluations(
    experiment_id: str,
    evaluations: schemas.ExperimentEvaluations,
    db: Session = Depends(get_db),
):
    return cruds.update_experiment_evaluation(
        db=db,
        experiment_id=experiment_id,
        evaluations=evaluations.evaluations,
    )


@router.post("/experiments/artifact-file-paths/{experiment_id}")
def update_artifact_file_paths(
    experiment_id: str,
    artifact_file_paths: schemas.ExperimentArtifactFilePaths,
    db: Session = Depends(get_db),
):
    return cruds.update_experiment_artifact_file_paths(
        db=db,
        experiment_id=experiment_id,
        artifact_file_paths=artifact_file_paths.artifact_file_paths,
    )
