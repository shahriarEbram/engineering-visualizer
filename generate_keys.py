import pickle
from pathlib import Path

import streamlit_authenticator as stauth

staff_names = ["hosseini", "babazadeh", "seydi"]
usernames = ["hosseini", "babazadeh", "seydi"]
passwords = ["Ho123h@", "Ba123b@", "Se123s@"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
