import enum


class PHYSICAL_SAVE_DATA(enum.Enum):
    NO_SAVE = 0
    SAVE = 1


class PREDICTION_TYPE(enum.Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class MODEL_RUNTIME(enum.Enum):
    SKLEARN = "sklearn"
    ONNX_RUNTIME = "onnx_runtime"
    ONNX_RUNTIME_SERVER = "onnx_runtime_server"
    TF_SERVING = "tf_serving"


class DATA_TYPE(enum.Enum):
    ARRAY = "array"
    IMAGE = "image"
    STRING = "string"


def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class _Constants(object):
    @constant
    def MODEL_DIRECTORY():
        return "/serving_patterns/models/"


CONSTANTS = _Constants()
