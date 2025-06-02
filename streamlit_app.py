import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import hashlib
import yaml
from yaml import SafeLoader

# Database connection
def get_db_connection():
    return sqlite3.connect('users.db')

# Hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authenticate user
def authenticate(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()

    if result:
        hashed_password = result[0]
        if hash_password(password) == hashed_password:
            return True
    return False

# Streamlit app
st.title('Login Page')

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(key='Login', location='main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')