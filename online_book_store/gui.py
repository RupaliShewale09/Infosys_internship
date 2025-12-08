import streamlit as st
from streamlit_option_menu import option_menu
import requests

st.set_page_config(page_title="Online Book Store", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
    <style>
    div[data-testid="stAlert"] {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

custom_style = """   
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stButton>button {
            background-color: #0e7c86;
            color: white;
            font-weight: bold;
            padding: 8px 20px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #095f66;
            color:white;
            font-size: 15px;
            transform: scale(1.03);
        }
        input {
            border-radius: 10px !important;
        }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- SIDEBAR ----------------
if not st.session_state.logged_in:
    with st.sidebar:

        selected = option_menu(
            menu_title=None,
            options=["Welcome", "Admin Login", "User Login / Register"],
            icons=["house", "person-check", "person"],
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "#0e7c86",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {
                    "background-color": "#0e7c86",
                    "color": "white",
                },
            },
        )
else:
    selected = None
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# ---------------- WELCOME ----------------
if not st.session_state.get("logged_in"):
    if selected == "Welcome":
        st.markdown("<h1 style='color:#0e7c86; text-align:center;'>📚 Welcome to <br> Online Book Store</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:20px; text-align:center;'>Your one-stop place for books of every genre.</h4>", unsafe_allow_html=True)
        st.markdown("""<p style='font-size:18px; margin-top:20px;'> Explore a wide collection of fiction, non-fiction, academic books, novels, and more. Browse, register, login, add books to cart, and place orders easily. </p>""", unsafe_allow_html=True)
        st.markdown("""<p style='font-size:18px; margin-top:15px; text-align:center;'>✨ <b>Start your reading journey today!</b></p>""", unsafe_allow_html=True)

# ---------------- ADMIN LOGIN ----------------
    elif selected == "Admin Login":
        col_left, col_mid, col_right = st.columns([2, 5, 2])
        with col_mid:
            st.markdown("<h3 style='text-align:center;'>🔐 Admin Login</h3>", unsafe_allow_html=True)

            with st.form("login_form"):
                admin_username = st.text_input("Username", key="admin_user")
                admin_password = st.text_input("Password", type="password", key="admin_pass")
                login_btn = st.form_submit_button("Login", use_container_width=True)


                if login_btn:
                    if not admin_username or not admin_password:
                            st.warning("⚠️ Please enter both username and password.")
                    else:
                        try:
                            response = requests.post(
                                f"{API_BASE}/admin/login",
                                json={"username": admin_username, "password": admin_password}
                            )
                            if response.status_code == 200:
                                st.success("Admin login successful!")
                                st.session_state.logged_in = True
                                st.session_state.user_type = "admin"
                                st.session_state.username = admin_username
                                st.rerun()
                            else:
                                st.error(response.json().get("detail", "Login failed"))
                        except Exception as e:
                            st.error(f"Backend not running or error: {e}")

# ---------------- USER LOGIN / REGISTER ----------------
    elif selected == "User Login / Register":
        col_left, col_mid, col_right = st.columns([2, 5, 2])
        with col_mid:
            st.markdown("<h3 style='text-align:center; color:#0e7c86;'>🔐 Login or Register</h3>", unsafe_allow_html=True)

            # form_type = st.radio("Choose", ["Login", "Sign Up"], horizontal=True)
            
            if "form_type" not in st.session_state:
                st.session_state.form_type = "login"

            def switch_to_signup():
                st.session_state.form_type = "signup"

            def switch_to_login():
                st.session_state.form_type = "login"

            # ---------------- LOGIN ----------------
            if st.session_state.form_type == "login":
                st.markdown("<h4 style='text-align:center;'>🧑‍💻 New user? Sign up below</h4>", unsafe_allow_html=True)
                st.button("Sign Up", on_click=switch_to_signup, use_container_width=True)
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align:center;'>🔐 Returning user? Login below</h4>", unsafe_allow_html=True)

                with st.form("user_login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Login", use_container_width=True)

                    if submitted:
                        if not username or not password:
                            st.warning("⚠️ Please enter both username and password.")
                        else:
                            try:
                                response = requests.post(f"{API_BASE}/user/login", json={"username": username, "password": password})
                                if response.status_code == 200:
                                    st.success("Login successful!")
                                    st.session_state.logged_in = True
                                    st.session_state.user_type = "user"
                                    st.session_state.username = username
                                    st.rerun()
                                else:
                                    st.error(response.json().get("detail", "Login failed"))
                            except Exception as e:
                                st.error(f"Backend not running: {e}")

            # ---------------- SIGN UP ----------------
            elif st.session_state.form_type == "signup":
                st.markdown("<h4 style='text-align:center;'>👋 New user? Register below</h4>", unsafe_allow_html=True)

                with st.form("user_signup_form"):
                    username = st.text_input("Username")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")

                    submitted = st.form_submit_button("Register", use_container_width=True)

                    if submitted:
                        if password != confirm_password:
                            st.error("❌ Passwords do not match!")
                        elif not all([username, email, password]):
                            st.warning("⚠️ All fields are required.")
                        else:
                            try:
                                response = requests.post(f"{API_BASE}/user/register", json={
                                    "username": username,
                                    "email": email,
                                    "password": password
                                })
                                if response.status_code in [200, 201]:
                                    st.success("Registration successful! Please log in to continue.")
                                else:
                                    try:
                                        msg = response.json().get("detail", "Registration failed")
                                    except:
                                        msg = "Registration failed"
                                    st.error(f"❌ {msg}")

                            except Exception as e:
                                st.error(f"Backend not running: {e}")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align:center; color:#0e7c86;'>Already have an account?</h4>", unsafe_allow_html=True)
                st.button("Back to Login", on_click=switch_to_login, use_container_width=True)



if st.session_state.get("logged_in") and st.session_state.user_type == "admin":
    st.markdown(f"<h2 style='color:#0e7c86; text-align:center;'>👋 Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)

    # Horizontal menu for admin actions
    menu_option = option_menu(
        menu_title=None,
        options=["Add Book", "Update Book Info", "View All Books", "Log out"],
        icons=["plus-circle", "pencil-square", "book", "door-closed"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "max-width": "900px",
                "margin": "0 auto",
                "padding": "0px",
                "background-color": "#fafafa",
                "display": "flex",
                "justify-content": "space-between",
                "width": "100%",
                "border-radius": "12px",
                "overflow": "hidden",
            },
            "icon": {"color": "orange", "font-size": "22px"},
            "nav-link": {
                "font-size": "16px",
                "color": "#0e7c86",
                "margin": "0px",
                "padding": "10px",
                "height": "120px",
                "width": "100%",
                "text-align": "center",
                "border": "1px solid #ccc",
                "border-radius": "0px",
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {
                "background-color": "#0e7c86",
                "color": "white",
            },
        }
    )

    # ------------------- LOGOUT -------------------
    if menu_option == "Log out":
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None
        st.rerun()

    elif menu_option == "Add Book":
        st.subheader("➕ Add a New Book")

        # Initialize session state for form fields if not already
        for field, default in [("add_name",""), ("add_author",""), ("add_description",""), ("add_copies",1), ("add_price",0.0)]:
            if field not in st.session_state:
                st.session_state[field] = default

        # Function to clear form fields
        def clear_form():
            st.session_state.add_name = ""
            st.session_state.add_author = ""
            st.session_state.add_description = ""
            st.session_state.add_copies = 1
            st.session_state.add_price = 0.0

        # --- FORM ---
        with st.form("add_book_form"):
            name = st.text_input("Book Name", key="add_name")
            author = st.text_input("Author", key="add_author")
            description = st.text_area("Description", key="add_description")
            copies = st.number_input("Copies", min_value=1, step=1, key="add_copies")
            price = st.number_input("Price", min_value=0.0, step=0.5, format="%.2f", key="add_price")

            # Buttons side by side
            col1, col2 = st.columns([0.5,5])
            with col1:
                submitted = st.form_submit_button("Add Book")
            with col2:
                clear = st.form_submit_button("Clear Fields", on_click=clear_form)

            # Handling Add Book
            if submitted:
                if not all([name, author, description]):
                    st.warning("⚠️ All fields are required.")
                else:
                    try:
                        res = requests.post(f"{API_BASE}/admin/add_book", json={
                            "name": name,
                            "author": author,
                            "description": description,
                            "copies": copies,
                            "price": price
                        })
                        if res.status_code == 200:
                            st.success(f"Book '{name}' added successfully! (ID: {res.json()['book_id']})")
                        else:
                            st.error(res.json().get("detail", "Failed to add book"))
                    except Exception as e:
                        st.error(f"Backend not running: {e}")


    # ------------------- UPDATE BOOK -------------------
    elif menu_option == "Update Book Info":
        st.subheader("✏️ Update Book Information")

        # Fetch all books first
        try:
            res = requests.get(f"{API_BASE}/admin/books")
            if res.status_code == 200:
                books_list = res.json().get("book_list", [])
                if not books_list:
                    st.info("No books available to update.")
                else:
                    # Dropdown to select book ID
                    book_ids = [b["book_id"] for b in books_list]
                    book_id = st.selectbox("Select Book ID to Update", options=book_ids)

                    # Update form
                    with st.form("update_book_form"):
                        name = st.text_input("Book Name (optional)")
                        author = st.text_input("Author (optional)")
                        description = st.text_area("Description (optional)")
                        copies = st.number_input("Copies (optional)", min_value=0, step=1)
                        price = st.number_input("Price (optional)", min_value=0.0, step=0.5, format="%.2f")
                        submitted = st.form_submit_button("Update Book")

                        if submitted:
                            data = {}
                            if name: data["name"] = name
                            if author: data["author"] = author
                            if description: data["description"] = description
                            if copies >= 0: data["copies"] = copies
                            if price > 0: data["price"] = price

                            if not data:
                                st.warning("⚠️ Enter at least one field to update.")
                            else:
                                try:
                                    res = requests.put(
                                        f"{API_BASE}/admin/update_book/{book_id}",
                                        json=data,
                                        timeout=5
                                    )

                                    if res.status_code == 200:
                                        try:
                                            response = res.json()
                                        except ValueError:
                                            st.error("⚠️ Backend returned non-JSON response.")
                                            response = {}

                                        # Backend returns updated_book dict
                                        if "updated_book" in response:
                                            updated_book = response["updated_book"]
                                            st.success(f"📖 Book ID {updated_book['book_id']} updated successfully!")
                                            st.markdown(f"""
                                            **Name:** {updated_book['name']}  
                                            **Author:** {updated_book['author']}  
                                            **Description:** {updated_book['description']}  
                                            **Copies Available:** {updated_book['copies']}  
                                            **Price:** ${updated_book['price']}
                                            """)

                                        else:
                                            st.success("Book updated successfully! (Backend returned no book details)")

                                    else:
                                        st.error(res.json().get("detail", "Failed to update book"))

                                except requests.exceptions.RequestException as e:
                                    st.error(f"Could not reach backend: {e}")

            else:
                st.error("Failed to fetch books.")
        except Exception as e:
            st.error(f"Backend error: {e}")



    # ------------------- VIEW ALL BOOKS -------------------
    elif menu_option == "View All Books":
        st.subheader("📚 All Books in the Store")
        try:
            res = requests.get(f"{API_BASE}/admin/books")
            if res.status_code == 200:
                books_list = res.json()["book_list"]
                if books_list:
                    for b in books_list:
                        st.markdown(f"**ID:** {b['book_id']}  |  **Name:** {b['name']}  |  **Author:** {b['author']}")
                        st.markdown(f"**Description:** {b['description']}")
                        st.markdown(f"**Remaining:** {b['remaining']}  |  **Sold:** {b['sold']}  |  **Price:** ${b['price']}")
                        st.markdown("---")
                else:
                    st.info("No books available.")
            else:
                st.error("Failed to fetch books.")
        except Exception as e:
            st.error(f"Backend not running: {e}")


# ------------------- USER MAIN MENU -------------------
elif st.session_state.get("logged_in") and st.session_state.user_type == "user":
    st.markdown(f"<h2 style='color:#0e7c86; text-align:center;'>👋 Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)

    # Horizontal menu for user actions
    menu_option = option_menu(
        menu_title=None,
        options=["Browse Books", "Search Books", "My Cart", "My Orders", "Log out"],
        icons=["book", "search", "cart", "clipboard-check", "door-closed"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "max-width": "900px",
                "margin": "0 auto",
                "padding": "0px",
                "background-color": "#fafafa",
                "display": "flex",
                "justify-content": "space-between",
                "border-radius": "12px",
            },
            "icon": {"color": "orange", "font-size": "22px"},
            "nav-link": {
                "font-size": "16px",
                "color": "#0e7c86",
                "margin": "0px",
                "padding": "10px",
                "height": "120px",
                "width": "100%",
                "text-align": "center",
                "border": "1px solid #ccc",
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
            },
            "nav-link-selected": {"background-color": "#0e7c86", "color": "white"},
        },
    )

    # ------------------- LOGOUT -------------------
    if menu_option == "Log out":
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None
        st.rerun()

    # ------------------- BROWSE BOOKS -------------------
    elif menu_option == "Browse Books":
        st.subheader("📚 All Available Books")
        try:
            res = requests.get(f"{API_BASE}/books")
            if res.status_code == 200:
                books_list = res.json()
                if books_list:
                    for b in books_list:
                        st.markdown(f"**ID:** {b['book_id']} | **Name:** {b['name']} | **Author:** {b['author']}")
                        st.markdown(f"**Description:** {b['description']}")
                        st.markdown(f"**Available Copies:** {b['copies']} | **Price:** ${b['price']}")
                        qty = st.number_input(f"Qty to add to cart (Book ID {b['book_id']})", min_value=1, max_value=b['copies'], key=f"user_qty_{b['book_id']}")
                        if st.button("Add to Cart", key=f"user_add_{b['book_id']}"):
                            try:
                                add_res = requests.post(f"{API_BASE}/cart/add", json={
                                    "username": st.session_state.username,
                                    "book_id": b['book_id'],
                                    "qty": qty
                                })
                                
                                if add_res.status_code == 200:
                                    st.success(f"Added {qty} copy(s) of '{b['name']}' to cart.")
                                else:
                                    st.error(add_res.json().get("detail", "Failed to add to cart"))
                            except Exception as e:
                                st.error(f"Backend error: {e}")
                        st.markdown("---")
                else:
                    st.info("No books available.")
            else:
                st.error("Failed to fetch books.")
        except Exception as e:
            st.error(f"Backend error: {e}")

    # ------------------- SEARCH BOOKS -------------------
    elif menu_option == "Search Books":
        st.subheader("🔍 Search Books by Name or Author")
        keyword = st.text_input("Enter book name or author")
        if st.button("Search"):
            if keyword.strip() == "":
                st.warning("Enter a keyword to search.")
            else:
                try:
                    res = requests.get(f"{API_BASE}/books/search", params={"keyword": keyword})
                    if res.status_code == 200:
                        results = res.json()
                        for b in results:
                            st.markdown(f"**ID:** {b['book_id']} | **Name:** {b['name']} | **Author:** {b['author']}")
                            st.markdown(f"**Description:** {b['description']}")
                            st.markdown(f"**Available Copies:** {b['copies']} | **Price:** ${b['price']}")
                            st.markdown("---")
                    else:
                        st.info("No matching books found.")
                except Exception as e:
                    st.error(f"Backend error: {e}")

    # ------------------- MY CART -------------------
    elif menu_option == "My Cart":
        st.subheader("🛒 My Cart")

        res = requests.get(f"{API_BASE}/cart/{st.session_state.username}")

        if res.status_code != 200 or not res.json().get("cart", []):
            st.info("Cart is empty.")
        else:
            cart = res.json().get("cart", [])

            if st.button("Clear Cart"):
                requests.post(
                    f"{API_BASE}/cart/clear",
                    json={"username": st.session_state.username}
                )
                st.rerun()
            
            all_books = requests.get(f"{API_BASE}/books").json()
            total = 0

            for item in cart:
                book = next((b for b in all_books if b["book_id"] == item["book_id"]), None)
                if not book:
                    continue

                col1, col2, col3 = st.columns([6, 2, 2])

                with col1:
                    st.markdown(f"**{book['name']}**")
                    st.write(f"Price: ₹{book['price']:.2f}")

                with col2:
                    new_qty = st.number_input(
                        f"Qty {book['book_id']}",
                        min_value=1,
                        max_value=book['copies'] ,
                        value=item["qty"],
                        step=1,
                        key=f"edit_qty_{book['book_id']}"
                    )

                subtotal = book["price"] * new_qty
                total += subtotal

                with col3:
                    st.write(f"₹{subtotal:.2f}")

                # Quantity Update Logic
                if new_qty != item["qty"]:
                    available = book['copies'] 

                    if new_qty > available:
                        st.error(f"Only {available} copies are available!")
                    else:
                        requests.post(
                            f"{API_BASE}/cart/update",
                            json={
                                "username": st.session_state.username,
                                "book_id": book["book_id"],
                                "qty": new_qty
                            }
                        )
                        st.rerun()

            st.markdown(f"## Total Amount: ₹{total:.2f}")

            if st.button("Proceed to Checkout"):
                try:
                    response = requests.post(f"{API_BASE}/order/checkout/{st.session_state.username}")
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Order placed successfully! ✅")
                        st.write(f"Order ID: {data['order_id']} | Total Amount: ₹{data['total_amount']:.2f}")
                        if st.button("Back to Menu"):
                            st.rerun()
                    else:
                        st.error(response.json().get("detail", "Checkout failed"))
                except Exception as e:
                    st.error(f"Checkout failed: {e}")


    elif menu_option == "My Orders":
        st.subheader("📦 Past Orders")

        res = requests.get(f"{API_BASE}/orders/{st.session_state.username}")

        if res.status_code != 200:
            st.info("No past orders.")
        else:
            orders_data = res.json().get("orders", [])
            books = requests.get(f"{API_BASE}/books").json()

            for order in orders_data:
                st.markdown(f"### Total: ₹{order['total_amount']:.2f}")
                
                for item in order["items"]:
                    book = next((b for b in books if b["book_id"] == item["book_id"]), None)
                    if book:
                        st.markdown(f"- **{book['name']}** | Qty: {item['qty']} | Price: ₹{item['price']:.2f}")
                st.markdown("---")

