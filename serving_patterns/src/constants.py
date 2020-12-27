import enum


class PLATFORM_ENUM(enum.Enum):
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    TEST = "test"


class JOB_ID_ENUM(enum.Enum):
    UUID = "uuid"
    INCREMENTAL = "incremental"
    UUID_INCREMENTAL = "uuid_incremental"


def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class _Constants(object):
    @constant
    def REDIS_INCREMENTS():
        return "increments"

    @constant
    def REDIS_QUEUE():
        return "redis_queue"


CONSTANTS = _Constants()
