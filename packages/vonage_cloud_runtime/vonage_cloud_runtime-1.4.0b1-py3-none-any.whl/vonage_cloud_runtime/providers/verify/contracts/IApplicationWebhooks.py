from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.verify.contracts.IApplicationStatusUrl import IApplicationStatusUrl


#interface
class IApplicationWebhooks(ABC):
    status_url:IApplicationStatusUrl
