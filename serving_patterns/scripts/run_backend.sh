#!/bin/bash

set -eu

BATCH_CODE=${APP_NAME:-"src.app.backend.prediction_batch"}

PYTHONPATH=./ python -m ${BATCH_CODE}
