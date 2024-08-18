import dataclasses
import datetime
import uuid


@dataclasses.dataclass
class Record:
    namespace: str
    payload: dict[str, str]
    created_at: datetime.datetime
    public_id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
