import sys, json, re

sys.path.append("..")  # Adds higher directory to python modules path.

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_conversation_read_wrong_path():
    """
    test that the /conversations endpoint doesnt return all conversations.
    """
    response = client.get("/conversations/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_conversation_read_start_empty():
    """
    at daemon start and with a empty db, no message is in a conversation
    """
    response = client.get("/conversations/test")
    assert response.status_code == 200
    assert response.json() == {"id": "test", "messages": []}


def test_conversation_create_message():
    """
    create a message in a conversation. validate there's only one message, and the timestamp format
    """
    response = client.post(
        "/messages/",
        headers={"Content-Type": "application/json"},
        json={"sender": "testuser", "message": "test message", "conversation_id": "testconvo"},
    )

    r = response.json()
    assert r["sender"] == "testuser"
    assert r["message"] == "test message"
    assert r["conversation_id"] == "testconvo"
    assert re.search(r"^\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$", r["created"])
    assert response.status_code == 200


def test_conversation_read_validate_one_message():
    """
    check that the conversation actually has only the message just created
    """
    response = client.get("/conversations/testconvo")
    assert response.status_code == 200
    assert len(response.json()["messages"]) == 1


def test_conversation_read_fixed_number_messages():
    """
    append three more messages to the conversation, check that we now have 4 messages.
    """

    for m in range(1, 4):  # three messages
        message = "test message n.{}".format(m)
        response = client.post(
            "/messages/",
            headers={"Content-Type": "application/json"},
            json={"sender": "testuser", "message": message, "conversation_id": "testconvo"},
        )

    response = client.get("/conversations/testconvo")
    assert response.status_code == 200
    assert len(response.json()["messages"]) == 4  # 1 previous + 3 just created
