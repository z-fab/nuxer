from qdrant_client import QdrantClient

from config.settings import SETTINGS as S


class QdrantExternal:
    def __init__(self):
        self.client = QdrantClient(
            host=S.QDRANT_HOST, port=S.QDRANT_PORT, api_key=S.QDRANT_API_KEY, https=False, prefer_grpc=True
        )

    def get_client(self) -> QdrantClient:
        return self.client
