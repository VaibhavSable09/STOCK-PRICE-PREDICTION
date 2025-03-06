import streamlit as st
from utils.auth import get_user_by_username

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access your profile")
    st.stop()

# Page config
st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
    layout="wide"
)

# Load custom CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get user data
user = get_user_by_username(st.session_state.username)

st.title("👤 User Profile")

# User info section
st.markdown("""
<div class="metric-card">
    <h3>Account Information</h3>
    <hr>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Username:** {user.username}")
    st.markdown(f"**Email:** {user.email}")
with col2:
    st.markdown(f"**Account Created:** {user.created_at.strftime('%Y-%m-%d')}")

st.markdown("</div>", unsafe_allow_html=True)

# Future features placeholder
st.markdown("### 🔜 Coming Soon")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>Watchlist</h4>
        <p>Create and manage your stock watchlist</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>Alert Settings</h4>
        <p>Set up price alerts for your favorite stocks</p>
    </div>
    """, unsafe_allow_html=True)
