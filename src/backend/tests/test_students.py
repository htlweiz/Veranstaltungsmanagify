import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from db.model import Student, Class, User
from api.main import app
from db.session import session
from crud.students import students
from api.model import StudentSchema

client = TestClient(app)

@pytest.fixture(scope="module")
def test_session():
    yield session
    session.rollback()
    for table in session.metadata.tables.values():
        session.execute(table.delete())
    session.commit()

@pytest.fixture(scope="module")
def test_user(test_session: Session):
    user = User(username="testuser", email="testuser@example.com", hashed_password="fakehashedpassword")
    test_session.add(user)
    test_session.commit()
    yield user
    test_session.delete(user)
    test_session.commit()

@pytest.fixture(scope="module")
def auth_token(test_user: User):
    return "saus"

@pytest.fixture(scope="module")
def authenticated_client(auth_token: str):
    client.cookies.set("Authorization", f"Bearer {auth_token}")
    yield client
    client.cookies.clear()

@pytest.fixture(scope="module")
def test_class(test_session: Session):
    test_class = Class(name="Test Class")
    test_session.add(test_class)
    test_session.commit()
    yield test_class
    test_session.delete(test_class)
    test_session.commit()

@pytest.fixture(scope="module")
def test_student(test_session: Session, test_class: Class):
    student_data = StudentSchema(
        first_name="John",
        last_name="Doe",
        is_female=False,
        class_name=test_class.name
    )
    student = students.create(student_data, user_creating_id=None)
    yield student
    test_session.delete(student)
    test_session.commit()

def test_create_student(authenticated_client: TestClient, test_session: Session, test_class: Class):
    student_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "is_female": True,
        "class_name": test_class.name
    }
    response = authenticated_client.post("/students", json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == student_data["first_name"]
    assert data["last_name"] == student_data["last_name"]
    assert data["is_female"] == student_data["is_female"]

def test_read_student(authenticated_client: TestClient, test_student: Student):
    response = authenticated_client.get(f"/students/{test_student.student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_student.first_name
    assert data["last_name"] == test_student.last_name
    assert data["is_female"] == test_student.is_female

def test_update_student(authenticated_client: TestClient, test_student: Student):
    update_data = {
        "first_name": "Johnny",
        "last_name": "Doe",
        "is_female": False,
        "class_name": test_student.my_class.name
    }
    response = authenticated_client.put(f"/students/{test_student.student_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]

def test_delete_student(authenticated_client: TestClient, test_student: Student):
    response = authenticated_client.delete(f"/students/{test_student.student_id}")
    assert response.status_code == 204
    response = authenticated_client.get(f"/students/{test_student.student_id}")
    assert response.status_code == 404