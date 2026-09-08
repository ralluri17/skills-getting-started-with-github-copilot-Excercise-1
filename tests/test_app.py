"""Tests for the Mergington High School API endpoints."""

CHESS_CLUB = "Chess Club"
EXISTING_EMAIL = "michael@mergington.edu"
NEW_EMAIL = "newstudent@mergington.edu"


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert CHESS_CLUB in data
    activity = data[CHESS_CLUB]
    assert set(activity.keys()) == {"description", "schedule", "max_participants", "participants"}


def test_signup_for_activity_success(client):
    response = client.post(f"/activities/{CHESS_CLUB}/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {NEW_EMAIL} for {CHESS_CLUB}"}

    activities_response = client.get("/activities").json()
    assert NEW_EMAIL in activities_response[CHESS_CLUB]["participants"]


def test_signup_for_activity_already_signed_up(client):
    response = client.post(f"/activities/{CHESS_CLUB}/signup", params={"email": EXISTING_EMAIL})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_unknown_activity(client):
    response = client.post("/activities/Not A Club/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_success(client):
    response = client.request(
        "DELETE", f"/activities/{CHESS_CLUB}/participants", params={"email": EXISTING_EMAIL}
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {EXISTING_EMAIL} from {CHESS_CLUB}"}

    activities_response = client.get("/activities").json()
    assert EXISTING_EMAIL not in activities_response[CHESS_CLUB]["participants"]


def test_unregister_participant_not_signed_up(client):
    response = client.request(
        "DELETE", f"/activities/{CHESS_CLUB}/participants", params={"email": NEW_EMAIL}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_unknown_activity(client):
    response = client.request(
        "DELETE", "/activities/Not A Club/participants", params={"email": EXISTING_EMAIL}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
