import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ExpirationExchange:
  book_id: int
  order_id: int
  status: str
  status_msg: str
  msg_type: str
  uuid: Optional[str] = None

  @property
  def subject(self) -> str:
    return 'expiration_exchange'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))
  
  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)