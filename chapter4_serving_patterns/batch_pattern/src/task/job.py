import time
from concurrent.futures import ThreadPoolExecutor
from logging import DEBUG, Formatter, StreamHandler, getLogger
from typing import Tuple

import numpy as np
from src.db import cruds, schemas
from src.db.database import get_context_db
from src.ml.prediction import classifier

logger = getLogger(__name__)
logger.setLevel(DEBUG)
strhd = StreamHandler()
strhd.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.addHandler(strhd)


def predict(item: schemas.Item) -> Tuple[int, np.ndarray]:
    prediction = classifier.predict(data=[item.values])
    logger.debug(f"prediction log: {item.id} {item.values} {prediction}")
    return item.id, prediction


def main():
    logger.info("waiting for batch to start")
    time.sleep(60)
    logger.info("starting batch")
    with get_context_db() as db:
        data = cruds.select_without_prediction(db=db)
        logger.info(f"predict data size: {len(data)}")
        predictions = {}
        with ThreadPoolExecutor(4) as executor:
            results = executor.map(predict, data)
        for result in results:
            predictions[result[0]] = list(result[1])
        cruds.register_predictions(
            db=db,
            predictions=predictions,
            commit=True,
        )
    logger.info("finished batch")


if __name__ == "__main__":
    main()
