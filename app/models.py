from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, constr


# input model for /messages/
class MessageIn(BaseModel):
    # conversation id, not message id
    conversation_id: constr(strip_whitespace=True, min_length=3, max_length=15)
    sender: constr(min_length=3, max_length=15)
    message: constr(min_length=2, max_length=50)
    created: Optional[constr(min_length=24, max_length=24)]

    class Config:
        orm_mode = True


# output model for messages in Conversations.
# only difference is
class MessageOut(BaseModel):
    sender: constr(min_length=3, max_length=15)
    message: constr(min_length=2, max_length=50)
    created: Optional[constr(min_length=24, max_length=24)]

    class Config:
        orm_mode = True


# output model for the conversation
class Conversation(BaseModel):
    # setting this to int for simplicity.
    id: str
    messages: List[MessageOut]

    class Config:
        orm_mode = True