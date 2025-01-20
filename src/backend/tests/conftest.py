import pytest
import datetime
import ssl
import pytest_asyncio
from starlette.testclient import TestClient
from db.session import session, metadata 
from api.main import app
from db.model import Note, User
import socketio

SERVER_URL = "https://127.0.0.1:8002"


# Utils
@pytest.fixture(autouse=True, scope="module")
def db_cleanup():
    yield
    session.rollback()
    for table in metadata.tables.values():
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope="module")
def test_app(user: User):
    client = TestClient(app, base_url=SERVER_URL)
    yield client


@pytest.fixture(scope="module")
def user():
    user = User(
        access_token = "abc",
        email = "ses@saus.gratis",
        password = "iyesss"
    )

    session.add(user)
    session.commit()

    yield user

    session.delete(user)


@pytest.fixture(scope="module")
def note(user: User):
    data = Note(
        title="Note title",
        content="Note content",
        public=True,
        user_id=user.user_id,
    )

    session.add(data)
    session.commit()

    yield data

    session.delete(data)

@pytest.fixture(scope="module")
def note_priv(user: User):
    note = Note(
        title="Note title",
        content="Note content",
        user_id=user.user_id,
        public=False,
        created=datetime.datetime.now(),
        changed=datetime.datetime.now()
    )

    session.add(note)
    session.commit()

    yield note

    session.delete(note)


@pytest_asyncio.fixture
async def sio_client(user: User):
    client = socketio.AsyncClient()
    headers = {
        "AccessToken": user.access_token
    }
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    await client.connect('{}'.format(SERVER_URL), headers=headers)
    yield client
    await client.disconnect()