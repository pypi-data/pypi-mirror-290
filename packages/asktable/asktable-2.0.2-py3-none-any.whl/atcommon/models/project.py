from atcommon.models.base import BaseCoreModel


class ProjectCore(BaseCoreModel):
    id: str
    name: str
    locked: int
    created_at: str
    modified_at: str

    __properties_init__ = ["id", "name", "created_at", "modified_at", "locked"]

    def __repr__(self):
        return f"<Project {self.id} [{self.name}]>"


class APIKeyCore(BaseCoreModel):
    id: str
    hashed_ak_value: str
    original_ak_value: str
    project_id: str
    status: int
    ak_role: str
    is_temp_token: int
    temp_token_payload: dict
    temp_token_expired_at: str
    last_used_at: str
    created_at: str

    __properties_init__ = [
        "id",
        "hashed_ak_value",
        "original_ak_value",
        "project_id",
        "status",
        "ak_role",
        "is_temp_token",
        "temp_token_payload",
        "temp_token_expired_at",
        "created_at",
        "last_used_at",
    ]

    def __repr__(self):
        return (
            f"<Token {self.id}({self.project_id})"
            f" [{self.status}-{self.last_used_at}]>"
        )

class JwtTokenCore(BaseCoreModel):
    user_id: int
    project_id: str
    ak_role: str
    is_temp_token: int
    temp_token_payload: dict
    is_user: bool

    __properties_init__ = [
        "user_id",
        "project_id",
        "ak_role",
        "is_temp_token",
        "temp_token_payload",
        "is_user",
    ]

    def __repr__(self):
        return (
            f"<project_id {self.project_id}, ak_role {self.ak_role}>"
        )