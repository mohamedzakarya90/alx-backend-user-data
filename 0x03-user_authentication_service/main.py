#!/usr/bin/env python3
"""
 The E2E integration test module
"""
from requests import get, put, post, delete


def register_user(email: str, password: str) -> None:
    """ the user registration test
    """
    # the new user which is successfully created
    request = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    response = request.json()
    assert response == {"email": email, "message": "user created"}
    assert request.status_code == 200

    # the email which is already associated with user
    request = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    response = request.json()
    assert response == {"message": "email already registered"}
    assert request.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """ the wrong password test
    """
    request = post("http://0.0.0.0:5000/sessions",
                   data={'email': email, "password": password})
    assert request.status_code == 401
    assert request.cookies.get("session_id") is None


def log_in(email: str, password: str) -> str:
    """ The login test
        Return->
             the session_id
    """
    request = post("http://0.0.0.0:5000/sessions",
                   data={'email': email, "password": password})
    response = request.json()
    session_id = request.cookies.get("session_id")
    assert request.status_code == 200
    assert response == {"email": email, "message": "logged in"}
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """ signed out the user profile test
    """
    request = get("http://0.0.0.0:5000/profile")
    assert request.status_code == 403


def profile_logged(session_id: str) -> None:
    """ signed in the user profile test
    """
    request = get("http://0.0.0.0:5000/profile",
                  cookies={"session_id": session_id})
    response = request.json()
    assert request.status_code == 200
    assert response == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ The logout test
    """
    request = delete("http://0.0.0.0:5000/sessions",
                     cookies={"session_id": session_id},
                     allow_redirects=True)
    response = request.json()
    history = request.history
    assert request.status_code == 200
    assert len(history) == 1
    assert history[0].status_code == 302
    assert response == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ resetting the token test
        Return->
              ther eset token
    """
    request = post("http://0.0.0.0:5000/reset_password",
                   data={"email": email})
    response = request.json()
    reset_token = response.get("reset_token")
    assert request.status_code == 200
    assert type(reset_token) is str
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ The password update test
    """
    request = put("http://0.0.0.0:5000/reset_password",
                  data={"email": email, "new_password":
                        new_password, "reset_token":
                        reset_token})
    response = request.json()
    assert request.status_code == 200
    assert response == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
