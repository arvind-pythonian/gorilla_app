import streamlit as st
import requests
from streamlit_jwt_authenticator import Authenticator
from constants import Constants


class Authenticate:
  def login(self, username, password):
    """
    Internal method to authenticate the user with provided credentials.

    Parameters:
    - username (str): The username for authentication.
    - password (str): The password for authentication.

    Returns:
    bool: True if authentication is successful, False otherwise.
    """
    if not username or not password:
      st.error("Please provide email and password")

    response = requests.request(
      method="POST",
      url=Constants.login_url,
      data={"email": username, "password": password},
      timeout=5
    )
    if not response.ok:
      st.error(f"Response: {response.status_code}. Detail {response.text}")
      return False
    st.session_state['authentication_status'] = True
    st.session_state["access"] = response.json()["access"]
    return True