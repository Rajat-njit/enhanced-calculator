import pytest
from app.operations import OperationFactory

def test_operation_factory_stub_raises():
    with pytest.raises(NotImplementedError):
        OperationFactory.create("add")
