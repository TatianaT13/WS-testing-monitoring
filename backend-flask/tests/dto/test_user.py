import pytest
from marshmallow import ValidationError

from backend.dto.user import UserCreationSchema


@pytest.mark.parametrize(
    "password,valid",
    [
        ("Abcde12345", True),
        ("12345Abcde", True),
        ("Abcdefghij", True),
        ("abcde12345", False),
        ("ABCDE12345", False),
        ("12345678", False),
        ("Abc123", False),
    ],
)
def test_validate_password(password, valid):
    # given
    schema = UserCreationSchema()
    data = {"username": "tetyana", "password": password, "email": "tetyana@mail.com"}

    # when
    try:
        user = schema.load(data)
        assert valid

        # then
        assert user is not None
        assert user.username == data["username"]
        assert user.password == password
        assert user.email == data["email"]
    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "email,valid",
    [
        ("tetyana@tetyana.com", True),
        ("tetyana@mail.fr", True),
        ("tetyana.tarasenko@mail.fr", True),
        ("tetyana.tarasenko@mail.mail.fr", True),
        ("tetyana@mail", False),
        ("tetyana.mail.com", False),
        ("tetyana@mail@com", False),
    ],
)
def test_validate_email(email, valid):
    # given
    schema = UserCreationSchema()
    data = {"username": "tetyana", "password": "Abcde12345", "email": email}

    # when
    try:
        user = schema.load(data)
        assert valid

        # then
        assert user is not None
        assert user.username == data["username"]
        assert user.password == data["password"]
        assert user.email == email
    except ValidationError:
        assert not valid


def test_missing_fields():
    # given
    schema = UserCreationSchema()
    data = {
        "username": "tetyana",
        "password": "Abcde12345",
    }

    # when / then
    with pytest.raises(ValidationError):
        schema.load(data)
