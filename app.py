import streamlit as st
import random
import string
import re
import pyperclip

# Page configuration
st.set_page_config(
    page_title="Password Manager",
    page_icon="🔐",
    layout="centered"
)

# Check if dark theme is enabled
theme = 'light'
try:
    if st.get_option("theme.base") == "dark":
        theme = 'dark'
except:
    pass

# Password history
password_history = []

# Custom CSS with dark mode support
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        color: white;
        background: linear-gradient(135deg, {"#2563EB" if theme == 'light' else "#64B5F6"}, {"#1E3A8A" if theme == 'light' else "#90CAF9"});
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1s ease-in-out;
    }}
    .tab-subheader {{
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.5rem 0;
        color: {("#2563EB" if theme == 'light' else "#64B5F6")};
        animation: slideIn 0.5s ease-in-out;
    }}
    .password-display {{
        font-family: monospace;
        padding: 20px;
        background-color: {("#F3F4F6" if theme == 'light' else "#2D3748")};
        border-radius: 12px;
        border: 2px solid {("#2563EB" if theme == 'light' else "#64B5F6")};
        font-size: 1.3rem;
        color: {("#000000" if theme == 'light' else "#FFFFFF")};
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1s ease-in-out;
    }}
    .result-container {{
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1s ease-in-out;
    }}
    .strong {{
        background-color: {("#ECFDF5" if theme == 'light' else "#0F3D2E")};
        border-left: 6px solid #10B981;
        color: {("#065F46" if theme == 'light' else "#ECFDF5")};
    }}
    .moderate {{
        background-color: {("#FFFBEB" if theme == 'light' else "#3D3000")};
        border-left: 6px solid #F59E0B;
        color: {("#92400E" if theme == 'light' else "#FFFBEB")};
    }}
    .weak {{
        background-color: {("#FEF2F2" if theme == 'light' else "#3D0000")};
        border-left: 6px solid #EF4444;
        color: {("#B91C1C" if theme == 'light' else "#FEF2F2")};
    }}
    .suggestion-item {{
        padding: 12px;
        background-color: {("#F3F4F6" if theme == 'light' else "#2D3748")};
        border-radius: 8px;
        margin: 10px 0;
        color: {("#1F2937" if theme == 'light' else "#E5E7EB")};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in-out;
    }}
    .footer {{
        text-align: center;
        margin-top: 2.5rem;
        padding: 1.5rem;
        background-color: {("#F3F4F6" if theme == 'light' else "#2D3748")};
        border-radius: 15px;
        color: {("#6B7280" if theme == 'light' else "#9CA3AF")};
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1s ease-in-out;
    }}
    .stTabs > div > div > button {{
        border: 2px solid {("#2563EB" if theme == 'light' else "#64B5F6")};
        border-radius: 10px;
        margin: 0 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in-out;
    }}
    @keyframes fadeIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
    @keyframes slideIn {{ 0% {{ transform: translateY(-20px); opacity: 0; }} 100% {{ transform: translateY(0); opacity: 1; }} }}
</style>
""", unsafe_allow_html=True)

def check_password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters long.")
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include at least one number.")
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Use at least one special character (!@#$%^&*).")
    if score == 5:
        return "🟢 Strong", "Your password meets all security requirements!", feedback, "strong"
    elif score >= 3:
        return "🟡 Moderate", "Your password is average. Consider improving it.", feedback, "moderate"
    else:
        return "🔴 Weak", "Your password needs improvement:", feedback, "weak"

def generate_password(length=12, use_digits=True, use_symbols=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in "!@#$%^&*" for c in password):
        pool += len("!@#$%^&*")
    entropy = len(password) * (pool.bit_length())
    return entropy

st.markdown('<div class="main-header">🔐 Password Manager</div>', unsafe_allow_html=True)
st.markdown("Enhance your online security with strong passwords")

tab1, tab2 = st.tabs(["🔍 Check Password", "🔑 Generate Password"])

with tab1:
    st.markdown('<div class="tab-subheader">Check Your Password Strength</div>', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            password = st.text_input("Enter password:", type="password", key="check_password")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            check_button = st.button("Check", use_container_width=True)
    if password:
        strength, message, feedback, strength_class = check_password_strength(password)
        st.markdown(f"""
        <div class="result-container {strength_class}">
            <h3>{strength}</h3>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
        if feedback:
            with st.container():
                st.subheader("Suggestions:")
                for tip in feedback:
                    st.markdown(f'<div class="suggestion-item">✓ {tip}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-subheader">Generate a Strong Password</div>', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            length = st.slider("🔢 Password length", 6, 32, 12)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            use_digits = st.checkbox("Include digits (123)", True)
            use_symbols = st.checkbox("Include symbols (!@#$)", True)
    generate_button = st.button("🚀 Generate Secure Password", type="primary", use_container_width=True)
    if generate_button:
        strong_password = generate_password(length, use_digits, use_symbols)
        password_history.insert(0, strong_password)
        entropy = calculate_entropy(strong_password)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-container strong">
            <h3>🔐 Your New Password</h3>
            <div class="password-display">{strong_password}</div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📋 Copy"):
                pyperclip.copy(strong_password)
                st.success("Password copied to clipboard!")
        with col2:
            st.markdown(f"🔐 Entropy Score: **{entropy} bits**")
        with st.expander("Password Details"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Length", f"{len(strong_password)} chars")
            col2.metric("Complexity", "High" if use_symbols and use_digits and length >= 12 else "Medium")
            col3.metric("Est. Strength", "Strong" if entropy >= 60 else "Moderate")
        with st.expander("🔁 Recently Generated Passwords"):
            if password_history:
                for i, p in enumerate(password_history[:5]):
                    st.code(p, language='bash')

st.markdown("""
<div class="footer">
    <p>Secure Password Manager v1.0 | Stay Safe Online | <a href="https://github.com/nadiaaGitHub">Created By Nadia</a> </p>
</div>
""", unsafe_allow_html=True)
