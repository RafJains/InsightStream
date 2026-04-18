from pydantic import BaseModel

class UserContentAction(BaseModel):
    user_id: int
    content_id: int

class ActionResponse(BaseModel):
    message: str 