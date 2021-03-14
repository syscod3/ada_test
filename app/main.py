from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.logger import logger as fastapi_logger
import logging

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from .models import MessageIn, Conversation
from .database import Base, MessageTable, get_db

from datetime import datetime

logger = logging.getLogger("gunicorn.error")
fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)

app = FastAPI(
    title="Ada Support Backend Coding Challenge",
    description="https://github.com/AdaSupport/backend-challenge",
    version="0.0.1",
)


@app.get("/")
def main():
    """ """
    return RedirectResponse(url="/docs/")


@app.post("/messages/", response_model=MessageIn)
async def message_submit(
    msg: MessageIn,
    db: Session = Depends(get_db),
):
    """
    Append a message to a given conversation id.
    'created' is optional, and will be added by the API
    with the current time.
    """

    # to adhere to the specified format as much as possible.
    # python's isoformat doesnt have Z$ as javascript.
    created = str(datetime.utcnow().isoformat(sep="T", timespec="milliseconds")) + "Z"
    msg.created = created
    record = MessageTable(
        conversation_id=msg.conversation_id,
        sender=msg.sender,
        message=msg.message,
        created=created,
    )
    db.add(record)
    db.commit()
    return msg


@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """
    Get all messages related to a given conversation id.
    """
    query = db.query(MessageTable).filter(MessageTable.conversation_id == conversation_id).all()
    Conversation.id = conversation_id
    Conversation.messages = query
    return Conversation
