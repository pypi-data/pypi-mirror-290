from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.verify.contracts.IApplicationVerify import IApplicationVerify


#interface
class IApplicationCapabilities(ABC):
    verify:IApplicationVerify
