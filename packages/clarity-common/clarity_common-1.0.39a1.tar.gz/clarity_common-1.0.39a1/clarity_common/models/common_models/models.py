from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ExecutionMetadata(BaseModel):
    execution_id: str
    agent_id: Optional[str] = None
    test_id: str
    step_id: str
    step_name: Optional[str] = None
    step_version: Optional[str] = None


class RunningEnvType(str, Enum):
    IOT = "iot_device"
    BATCH = "batch"


'''Execution definitions'''


class PackageType(str, Enum):
    # Supported types for test step deployment
    PIP = "PIP"
    ZIP = "ZIP"


class MessageType(str, Enum):
    # Supported types for test step deployment
    LOG = "LOG"
    TEST_STATE = "TEST_STATE"
    EXECUTION_STATE = "EXECUTION_STATE"
    FINDING = "FINDING"
    TEST_ARTIFACT = "TEST_ARTIFACT"
    EXECUTION_OUTPUT = "EXECUTION_OUTPUT"
