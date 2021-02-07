from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import JSON
from src.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String(255), primary_key=True)
    project_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class Model(Base):
    __tablename__ = "models"

    model_id = Column(String(255), primary_key=True)
    project_id = Column(
        String(255),
        ForeignKey("projects.project_id"),
        nullable=False,
    )
    model_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(String(255), primary_key=True)
    model_version_id = Column(String(255), nullable=False)
    model_id = Column(
        String(255),
        ForeignKey("models.model_id"),
        nullable=False,
    )
    parameters = Column(JSON, nullable=True)
    training_dataset = Column(Text, nullable=True)
    validation_dataset = Column(Text, nullable=True)
    test_dataset = Column(Text, nullable=True)
    evaluations = Column(JSON, nullable=True)
    artifact_file_paths = Column(JSON, nullable=True)
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
