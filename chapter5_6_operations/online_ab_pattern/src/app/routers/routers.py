from fastapi import APIRouter
from typing import Dict, List, Any
import uuid
from logging import getLogger
from src.ml.prediction import classifier, Data
from src.configurations import ModelConfigurations

logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "float32",
        "data_structure": "(1,4)",
        "data_sample": Data().data,
        "prediction_type": "float32",
        "prediction_structure": "(1,3)",
        "prediction_sample": [0.97093159, 0.01558308, 0.01348537],
    }


@router.get("/label")
def label() -> Dict[int, str]:
    return classifier.label


@router.get("/predict/test")
async def predict_test() -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())[:6]
    prediction = await classifier.predict(data=Data().data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction_list}")
    return {"prediction": prediction_list, "mode": ModelConfigurations.mode}


@router.get("/predict/test/label")
async def predict_test_label() -> Dict[str, str]:
    job_id = str(uuid.uuid4())[:6]
    prediction = await classifier.predict_label(data=Data().data)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction}")
    return {"prediction": prediction, "mode": ModelConfigurations.mode}


@router.post("/predict")
async def predict(data: Data) -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())[:6]
    prediction = await classifier.predict(data.data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction_list}")
    return {"prediction": prediction_list, "mode": ModelConfigurations.mode}


@router.post("/predict/label")
async def predict_label(data: Data) -> Dict[str, str]:
    job_id = str(uuid.uuid4())[:6]
    prediction = await classifier.predict_label(data.data)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction}")
    return {"prediction": prediction, "mode": ModelConfigurations.mode}
