from typing import Optional
from collections import defaultdict


class UserRepository:
    def get_user_context(self, user_id: int) -> Optional[list]:
        raise NotImplementedError

    def add_user_context(self, user_id: int, context: str) -> None:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.user_data = defaultdict(lambda: [])

    def get_user_context(self, user_id: int) -> list:
        return self.user_data[user_id]

    def add_user_context(self, user_id: int, context: str) -> None:
        self.user_data[user_id].append(context)
