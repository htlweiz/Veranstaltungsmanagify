from db.session import session
from db.model import Note, User
from api.model import NoteSchema, NotePatch, NoteDB
from crud.notes import notes
from starlette.testclient import TestClient


def test_create_note_db(user: User):
    data = NoteSchema(title='test', content='test', public=False)
    note: Note = notes.create(data, user_creating_id=user.user_id)

    assert note.note_id is not None
    assert note.title == data.title 
    assert note.content == data.content 
    assert note.public == data.public

def test_put_note_db(note: Note):
    data = NoteSchema(title='test1', content=note.content, public=note.public)
    updated_note: Note = notes.put(note.note_id, data)

    assert updated_note.note_id == note.note_id
    assert updated_note.title == data.title
    assert updated_note.content == note.content
    assert updated_note.public == note.public

def test_patch_note_db(note: Note):
    data = NotePatch(title='test28')
    updated_note: Note = notes.patch(note.note_id, data)

    assert updated_note.note_id == note.note_id
    assert updated_note.title == data.title
    assert updated_note.content == note.content
    assert updated_note.public == note.public

def test_delete_note_db(note: Note):
    notes.delete(note)
    assert session.query(Note).filter(Note.note_id == note.note_id).first() is None

def test_create_note_request(test_app: TestClient, monkeypatch, user: User, note: Note):
    data = {'title': 'test', 'content': 'test', 'public': False}

    def mock_post(_, __):
        return note

    monkeypatch.setattr(notes, "create", mock_post)

    response = test_app.post('/notes', json=data, headers={'AccessToken': f'{user.access_token}'})

    assert response.status_code == 201

def test_put_note_request(test_app: TestClient, monkeypatch, note: Note, user: User):
    data = {'title': 'test1', 'content': note.content, 'public': note.public}

    def mock_put(_, __):
        return note

    monkeypatch.setattr(notes, "put", mock_put)

    response = test_app.put(f'/notes/{note.note_id}', json=data, headers={'AccessToken': f'{user.access_token}'})

    assert response.status_code == 200

def test_patch_note_request(test_app: TestClient, monkeypatch, note: Note, user: User):
    data = {'title': 'test28'}

    def mock_patch(_, __):
        return note

    monkeypatch.setattr(notes, "patch", mock_patch)

    response = test_app.patch(f'/notes/{note.note_id}', json=data, headers={'AccessToken': f'{user.access_token}'})

    assert response.status_code == 200

def test_delete_note_request(test_app: TestClient, monkeypatch, note: Note, user: User):
    def mock_delete(_):
        pass

    monkeypatch.setattr(notes, "delete_by_id", mock_delete)

    response = test_app.delete(f'/notes/{note.note_id}', headers={'AccessToken': f'{user.access_token}'})

    assert response.status_code == 204