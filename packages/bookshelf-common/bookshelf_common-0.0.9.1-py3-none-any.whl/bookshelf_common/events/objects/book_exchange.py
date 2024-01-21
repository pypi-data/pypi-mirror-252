import json
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class BookExchange:
  id: int
  title: str
  slug: str
  novelist: str
  description: str
  price: int
  status: str
  genre: str
  user_id: int
  version: int
  action: str = 'create'
  uuid: Optional[str] = None

  @property
  def subject(self) -> str:
    return 'book_exchange'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))

  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)