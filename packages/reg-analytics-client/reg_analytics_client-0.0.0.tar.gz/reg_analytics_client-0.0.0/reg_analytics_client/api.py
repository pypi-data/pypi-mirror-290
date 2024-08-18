import httpx
import marshmallow_recipe as mr

from .data import Record


class Client:
    async def persist(self, record: Record) -> None:
        data = mr.dump(record)
        response = await self.client.post("api/analytics", json=data)
        if response.status_code == 201:
            return
        if response.status_code == 400:
            raise self.AlreadyExists

    class AlreadyExists(BaseException):
        pass

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
