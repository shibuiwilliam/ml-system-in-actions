from logging import getLogger
from typing import Any, Dict, List

from fastapi import APIRouter
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
        "prediction_structure": "(1,3)",
        "prediction_sample": [0.97093159, 0.01558308, 0.01348537],
    }


@router.get("/label")
def label() -> Dict[int, str]:
    return classifier.label


@router.get("/predict/test")
def predict_test() -> Dict[str, List[float]]:
    prediction = classifier.predict(data=Data().data)
    return {"prediction": list(prediction)}


@router.get("/predict/test/label")
def predict_test_label() -> Dict[str, str]:
    prediction = classifier.predict_label(data=Data().data)
    return {"prediction": prediction}


@router.post("/predict")
def predict(data: Data) -> Dict[str, List[float]]:
    prediction = classifier.predict(data.data)
    return {"prediction": list(prediction)}


@router.post("/predict/label")
def predict_label(data: Data) -> Dict[str, str]:
    prediction = classifier.predict_label(data.data)
    return {"prediction": prediction}
