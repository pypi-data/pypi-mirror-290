from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.verify.contracts.IApplicationWebhooks import IApplicationWebhooks


#interface
class IApplicationVerify(ABC):
    webhooks:IApplicationWebhooks
    version:str
