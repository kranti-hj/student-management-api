
import pytest
import app as api


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_students.db"
    monkeypatch.setattr(api, "DATABASE", test_db)
    api.init_db()
    api.app.config.update(TESTING=True)

    with api.app.test_client() as test_client:
        yield test_client


def sample_student(email="rahul@example.com"):
    return {
        "name": "Rahul Sharma",
        "email": email,
        "course": "CSE Data Science",
        "age": 21
    }


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_and_read_student(client):
    response = client.post(
        "/api/students", json=sample_student()
    )
    assert response.status_code == 201

    student_id = response.get_json()["id"]
    response = client.get(f"/api/students/{student_id}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Rahul Sharma"


def test_invalid_input(client):
    response = client.post(
        "/api/students", json={"name": "Rahul"}
    )
    assert response.status_code == 400


def test_duplicate_email(client):
    client.post("/api/students", json=sample_student())
    response = client.post(
        "/api/students", json=sample_student()
    )
    assert response.status_code == 409


def test_update_student(client):
    created = client.post(
        "/api/students", json=sample_student()
    )
    student_id = created.get_json()["id"]

    data = sample_student()
    data["course"] = "Artificial Intelligence"

    response = client.put(
        f"/api/students/{student_id}", json=data
    )

    assert response.status_code == 200
    assert response.get_json()["course"] == "Artificial Intelligence"


def test_delete_student(client):
    created = client.post(
        "/api/students", json=sample_student()
    )
    student_id = created.get_json()["id"]

    response = client.delete(f"/api/students/{student_id}")
    assert response.status_code == 200

    response = client.get(f"/api/students/{student_id}")
    assert response.status_code == 404