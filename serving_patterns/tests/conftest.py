import pytest


@pytest.fixture(scope="session", autouse=False)
def scope_session():
    print("\nsetup before session.\n")
    yield
    print("\nteardown after session.\n")


@pytest.fixture(scope="module", autouse=False)
def scope_module():
    print("\nsetup before module.\n")
    yield
    print("\nteardown after module.\n")


@pytest.fixture(scope="class", autouse=False)
def scope_class():
    print("\nsetup before class.\n")
    yield
    print("\nteardown after class.\n")


@pytest.fixture(scope="function", autouse=False)
def scope_function():
    print("\nsetup before function.\n")
    yield
    print("\nteardown after function.\n")
