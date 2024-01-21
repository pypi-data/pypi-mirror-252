from dataclasses import dataclass, asdict
import json

@dataclass
class PaymentExchange:
  order_id: int
  payment_id: str
  price: str
  status: str = 'completed'

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