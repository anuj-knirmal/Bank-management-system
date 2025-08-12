import json
import random
import string
from pathlib import Path
import streamlit as st

# ======== Custom CSS for Attractive UI ==========
st.markdown("""
    <style>
    .title {
        font-size: 36px !important;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .account-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ======== Bank Class ==========
class Bank:
    database = 'data.json'

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            try:
                with open(cls.database) as fs:
                    return json.load(fs)
            except json.JSONDecodeError:
                return []
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, 'w') as fs:
            json.dump(data, fs, indent=4)

    @staticmethod
    def generate_account_number():
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%&", k=1)
        acc_id = alpha + num + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    @classmethod
    def find_user(cls, acc_no, pin):
        data = cls.load_data()
        for user in data:
            if user['accountNo'] == acc_no and str(user['pin']) == str(pin):
                return user
        return None

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18:
            return False, "❌ Age must be at least 18."
        if len(str(pin)) != 4:
            return False, "❌ PIN must be exactly 4 digits."

        data = cls.load_data()
        new_account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": str(pin),  # Store as string
            "accountNo": cls.generate_account_number(),
            "Balance": 0
        }
        data.append(new_account)
        cls.save_data(data)
        return True, new_account

    @classmethod
    def deposit_money(cls, acc_no, pin, amount):
        if amount <= 0 or amount > 10000:
            return False, "❌ Deposit must be between 1 and 10,000."

        data = cls.load_data()
        for user in data:
            if user['accountNo'] == acc_no and str(user['pin']) == str(pin):
                user['Balance'] += amount
                cls.save_data(data)
                return True, f"✅ Deposited ₹{amount} successfully."
        return False, "❌ Account not found or incorrect PIN."

    @classmethod
    def withdraw_money(cls, acc_no, pin, amount):
        data = cls.load_data()
        for user in data:
            if user['accountNo'] == acc_no and str(user['pin']) == str(pin):
                if user['Balance'] < amount:
                    return False, "❌ Insufficient balance."
                user['Balance'] -= amount
                cls.save_data(data)
                return True, f"✅ Withdrew ₹{amount} successfully."
        return False, "❌ Account not found or incorrect PIN."

    @classmethod
    def update_details(cls, acc_no, pin, name=None, email=None, new_pin=None):
        data = cls.load_data()
        for user in data:
            if user['accountNo'] == acc_no and str(user['pin']) == str(pin):
                if name: user['name'] = name
                if email: user['email'] = email
                if new_pin:
                    if len(str(new_pin)) != 4:
                        return False, "❌ New PIN must be 4 digits."
                    user['pin'] = str(new_pin)
                cls.save_data(data)
                return True, "✅ Details updated successfully."
        return False, "❌ Account not found or incorrect PIN."

    @classmethod
    def delete_account(cls, acc_no, pin):
        data = cls.load_data()
        for i, user in enumerate(data):
            if user['accountNo'] == acc_no and str(user['pin']) == str(pin):
                data.pop(i)
                cls.save_data(data)
                return True, "✅ Account deleted successfully."
        return False, "❌ Account not found or incorrect PIN."

# ======== Streamlit UI ==========
st.markdown('<p class="title">🏦 Modern Bank System</p>', unsafe_allow_html=True)

menu = ["🏠 Home", "➕ Create Account", "💰 Deposit", "💸 Withdraw", "📜 View Details", "✏️ Update Details", "🗑️ Delete Account"]
choice = st.sidebar.radio("Select Action", menu)

if choice == "🏠 Home":
    st.subheader("Welcome to the Modern Bank App 💳")
    st.write("Use the sidebar to perform actions.")
    st.info("All PIN fields are hidden for your security.")

elif choice == "➕ Create Account":
    with st.form("create_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0)
        email = st.text_input("Email")
        pin = st.text_input("4-digit PIN", type="password")
        submit = st.form_submit_button("Create Account")
    if submit:
        success, result = Bank.create_account(name, age, email, pin)
        if success:
            st.success("✅ Account created successfully!")
            st.markdown(f"<div class='account-box'>Account Number: <b>{result['accountNo']}</b></div>", unsafe_allow_html=True)
        else:
            st.error(result)

elif choice == "💰 Deposit":
    with st.form("deposit_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=0)
        submit = st.form_submit_button("Deposit Money")
    if submit:
        success, msg = Bank.deposit_money(acc_no, pin, amount)
        st.success(msg) if success else st.error(msg)

elif choice == "💸 Withdraw":
    with st.form("withdraw_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=0)
        submit = st.form_submit_button("Withdraw Money")
    if submit:
        success, msg = Bank.withdraw_money(acc_no, pin, amount)
        st.success(msg) if success else st.error(msg)

elif choice == "📜 View Details":
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show Details"):
        user = Bank.find_user(acc_no, pin)
        if user:
            st.markdown("<div class='account-box'>", unsafe_allow_html=True)
            st.write(user)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Account not found or incorrect PIN.")

elif choice == "✏️ Update Details":
    with st.form("update_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("Current PIN", type="password")
        name = st.text_input("New Name (optional)")
        email = st.text_input("New Email (optional)")
        new_pin = st.text_input("New 4-digit PIN (optional)", type="password")
        submit = st.form_submit_button("Update")
    if submit:
        success, msg = Bank.update_details(acc_no, pin, name or None, email or None, new_pin or None)
        st.success(msg) if success else st.error(msg)

elif choice == "🗑️ Delete Account":
    with st.form("delete_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        submit = st.form_submit_button("Delete Account")
    if submit:
        success, msg = Bank.delete_account(acc_no, pin)
        st.success(msg) if success else st.error(msg)
