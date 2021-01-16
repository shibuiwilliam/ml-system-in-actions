import uuid
from logging import getLogger
from typing import Any, Dict, List

from fastapi import APIRouter
from src.configurations import ModelConfigurations
from src.ml.prediction import Data, classifier

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
        "prediction_structure": "(1,2)",
        "prediction_sample": [0.970000, 0.030000],
    }


@router.get("/predict/test")
def predict_test(id: str = str(uuid.uuid4())[:6]) -> Dict[str, List[float]]:
    prediction = classifier.predict(data=Data().data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode_name} {id}: {prediction_list}")
    return {"prediction": prediction_list}


@router.post("/predict")
def predict(data: Data, id: str = str(uuid.uuid4())[:6]) -> Dict[str, List[float]]:
    prediction = classifier.predict(data.data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode_name} {id}: {prediction_list}")
    return {"prediction": prediction_list}
