"""
Test suite for Mergington High School Activities API
Using Arrange-Act-Assert (AAA) pattern for all tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture to provide a TestClient for the FastAPI app.
    Creates a fresh client for each test to ensure test isolation.
    """
    return TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_returns_200(self, client):
        """
        Arrange: Set up test client
        Act: Send GET request to /activities
        Assert: Response status is 200 OK
        """
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_all_activities_returns_dict_of_activities(self, client):
        """
        Arrange: Set up test client
        Act: Send GET request to /activities
        Assert: Response is a dictionary with activity data
        """
        # Arrange
        # (implicit in fixture)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_get_activities_contains_required_fields(self, client):
        """
        Arrange: Set up test client
        Act: Send GET request to /activities
        Assert: Each activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing '{field}'"

    def test_get_activities_participants_is_list(self, client):
        """
        Arrange: Set up test client
        Act: Send GET request to /activities
        Assert: Participants field is a list for each activity
        """
        # Arrange
        # (implicit in fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(
                activity_data["participants"], list
            ), f"Activity '{activity_name}' participants is not a list"


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_valid_activity_returns_200(self, client):
        """
        Arrange: Set up test client with a valid activity and email
        Act: Send POST request to signup endpoint
        Assert: Response status is 200 OK
        """
        # Arrange
        activity_name = "Chess Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200

    def test_signup_valid_activity_returns_success_message(self, client):
        """
        Arrange: Set up test client with a valid activity and email
        Act: Send POST request to signup endpoint
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """
        Arrange: Set up test client and get initial participant count
        Act: Send POST request to signup endpoint
        Assert: Participant is added to the activity
        """
        # Arrange
        activity_name = "Programming Class"
        email = "testuser@mergington.edu"

        # Get initial state
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)

        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Get updated state
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        updated_count = len(updated_participants)

        # Assert
        assert updated_count == initial_count + 1
        assert email in updated_participants

    def test_signup_invalid_activity_returns_404(self, client):
        """
        Arrange: Set up test client with an invalid activity name
        Act: Send POST request to signup endpoint
        Assert: Response status is 404 Not Found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404

    def test_signup_invalid_activity_returns_error_message(self, client):
        """
        Arrange: Set up test client with an invalid activity name
        Act: Send POST request to signup endpoint
        Assert: Response contains error detail
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestUnregisterFromActivity:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_valid_participant_returns_200(self, client):
        """
        Arrange: Set up test client with an activity and participant
        Act: Send POST request to unregister endpoint
        Assert: Response status is 200 OK
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Known participant from app.py

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200

    def test_unregister_valid_participant_returns_success_message(self, client):
        """
        Arrange: Set up test client with an activity and participant
        Act: Send POST request to unregister endpoint
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Gym Class"
        email = "olivia@mergington.edu"  # Known participant from app.py

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant_from_activity(self, client):
        """
        Arrange: Set up test client and get initial participant count
        Act: Send POST request to unregister endpoint
        Assert: Participant is removed from the activity
        """
        # Arrange
        activity_name = "Drama Club"
        email = "jordan@mergington.edu"  # Known participant from app.py

        # Get initial state
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)

        # Act
        client.post(f"/activities/{activity_name}/unregister?email={email}")

        # Get updated state
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        updated_count = len(updated_participants)

        # Assert
        assert updated_count == initial_count - 1
        assert email not in updated_participants

    def test_unregister_invalid_activity_returns_404(self, client):
        """
        Arrange: Set up test client with an invalid activity name
        Act: Send POST request to unregister endpoint
        Assert: Response status is 404 Not Found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_nonexistent_participant_returns_404(self, client):
        """
        Arrange: Set up test client with a valid activity but non-existent participant
        Act: Send POST request to unregister endpoint
        Assert: Response status is 404 Not Found
        """
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_nonexistent_participant_returns_error_message(self, client):
        """
        Arrange: Set up test client with a valid activity but non-existent participant
        Act: Send POST request to unregister endpoint
        Assert: Response contains error detail
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notfound@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "not found" in data["detail"].lower()
