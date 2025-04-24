import uuid
from urllib.parse import parse_qs, urlparse

import redis
import tiktoken


class Hippocampus:
    """
    A class representing the hippocampus, a region of the brain associated with memory and spatial navigation.
    """

    def __init__(self):
        """
        Initializes the Hippocampus object.
        """
        self.redis_client: redis.Redis
        self.memory_context_length = 8000  # 8000 tokens
        self.memory = []

    def memory_established(self, redis_url: str):
        parsed_url = urlparse(redis_url)
        if parsed_url.scheme != "redis":
            raise ValueError("Invalid Redis URL scheme. Expected 'redis'.")
        host = parsed_url.hostname
        port = parsed_url.port
        qs = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        self.redis_client = redis.StrictRedis(host=host, port=port, db=int(qs["db"]))

    def _count_token(self, content: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(content)
        return len(tokens)

    def _trim(self):
        list_key = "chat:messages"
        token_key = "chat:tokens"
        content_key = "chat:contents"

        # Get the number of tokens for each message ID
        counts = {
            k.decode(): int(v) for k, v in self.redis_client.hgetall(token_key).items()
        }

        # Fetch the full list of IDs (newest→oldest)
        msg_ids = [mid.decode() for mid in self.redis_client.lrange(list_key, 0, -1)]
        total_token = sum(counts.get(mid, 0) for mid in msg_ids)

        # While over budget, pop oldest
        #   (oldest is at the tail of the list)
        while total_token > self.memory_context_length and msg_ids:
            oldest_msg_id = msg_ids.pop()
            trimmed_token = counts.get(oldest_msg_id, 0)

            self.redis_client.lrem(list_key, 1, oldest_msg_id)
            self.redis_client.hdel(token_key, oldest_msg_id)
            self.redis_client.hdel(content_key, oldest_msg_id)

            total_token -= trimmed_token

    def clear_memory(self):
        """
        Clears all memory stored in the hippocampus.
        """
        self.redis_client.flushdb()
        self.redis_client.close()

    def store_memory(self, role: str, content: str):
        """
        Stores a memory in the hippocampus.
        """
        num_token = self._count_token(content)
        msg_id = str(uuid.uuid4())

        content_key = "chat:contents"
        self.redis_client.hset(content_key, msg_id, f"{role}|{content}")
        token_key = "chat:tokens"
        self.redis_client.hset(token_key, msg_id, num_token)
        message_list_key = "chat:messages"
        self.redis_client.lpush(message_list_key, msg_id)

        self._trim()

    def recall_memory(self) -> list(dict[str, str]):
        """
        Recalls the most recent memory stored in the hippocampus.

        Returns:
            str: The most recent memory.
        """
        list_key = "chat:messages"
        content_key = "chat:contents"

        # Get all IDs (newest→oldest), then reverse for oldest→newest
        ids = [mid.decode() for mid in self.redis_client.lrange(list_key, 0, -1)]
        ids.reverse()

        raw = []
        if ids:
            raw = self.redis_client.hmget(content_key, ids)

        # Split into role and content
        window = []
        for item in raw:
            if item is None:
                continue
            role, content = item.decode().split("|", 1)
            window.append({"role": role, "content": content})

        return window
