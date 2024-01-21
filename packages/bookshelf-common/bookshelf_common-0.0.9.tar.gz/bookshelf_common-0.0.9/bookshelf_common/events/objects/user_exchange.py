import json
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class UserExchange:
  id: int
  email: str
  first_name: str
  last_name: str
  address: str
  city: str
  phone: str
  action: str = 'create'
  uuid: Optional[str] = None

  @property
  def subject(self) -> str:
    return 'user_exchange'

  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))
  
  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)