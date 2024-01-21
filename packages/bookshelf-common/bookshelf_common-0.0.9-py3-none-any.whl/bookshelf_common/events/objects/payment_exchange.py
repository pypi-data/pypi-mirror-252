import json
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class PaymentExchange:
  order_id: int
  payment_id: str
  price: str
  status: str = 'completed'
  uuid: Optional[str] = None

  @property
  def subject(self) -> str:
    return 'payment_exchange'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))

  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)