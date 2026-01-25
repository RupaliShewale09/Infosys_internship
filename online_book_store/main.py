from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

admin_username = "library"
admin_password = "1234"


# Pydantic Models-----------------------------------------------------------------
class Book(BaseModel):
    name: str
    author: str
    description: str
    copies: int
    price: float

class BookUpdate(BaseModel):
    name: str | None = None
    author: str | None = None
    description: str | None = None
    copies: int | None = None
    price: float | None = None

class User(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class CartItem(BaseModel):
    book_id: int
    qty: int

class AddToCart(BaseModel):
    username: str
    book_id: int
    qty: int


# ADMIN ROUTES-----------------------------------------------------------------
@app.post("/admin/login")
def admin_login(user: Login):
    # Check credentials
    if user.username == admin_username and user.password == admin_password:
        return {"message": "Admin login successful"}

    raise HTTPException(status_code=401, detail="Invalid Admin Credentials")


@app.post("/admin/add_book")
def add_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (name, author, description, copies, price) VALUES (%s,%s,%s,%s,%s)",
        (book.name, book.author, book.description, book.copies, book.price)
    )
    conn.commit()
    book_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"message": "Book added", "book_id": book_id}


@app.put("/admin/update_book/{book_id}")
def update_book(book_id: int, details: BookUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    data = details.dict(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No update data provided")

    set_str = ", ".join([f"{k}=%s" for k in data.keys()])
    values = list(data.values())
    values.append(book_id)

    cursor.execute(f"UPDATE books SET {set_str} WHERE book_id=%s", values)
    conn.commit()

    cursor.execute("SELECT book_id, name, author, description, copies, price FROM books WHERE book_id=%s", (book_id,))
    updated_book = cursor.fetchone()

    cursor.close()
    conn.close()

    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found after update")

    updated_book_dict = {
        "book_id": updated_book["book_id"],
        "name": updated_book["name"],       
        "author": updated_book["author"],
        "description": updated_book["description"],
        "copies": updated_book["copies"],  
        "price": updated_book["price"]
    }

    return {
        "message": "Book updated",
        "updated_book": updated_book_dict
    }


@app.get("/admin/books")
def admin_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books_list = cursor.fetchall()

    for b in books_list:
        cursor.execute("SELECT SUM(qty) as sold FROM order_items WHERE book_id=%s", (b["book_id"],))
        sold = cursor.fetchone()["sold"] or 0
        b["sold"] = sold
        b["remaining"] = b["copies"]
    cursor.close()
    conn.close()
    return {"total_books": len(books_list), "book_list": books_list}


# USER ROUTES-----------------------------------------------------------------
@app.post("/user/register")
def register(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (user.username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                   (user.username, user.email, user.password))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User registered successfully"}


@app.post("/user/login")
def user_login(user: Login):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user.username, user.password))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {"message": "User login successful"}
    cursor.close()
    conn.close()
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/books")
def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return books_list


@app.get("/books/search")
def search_book(keyword: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE name LIKE %s OR author LIKE %s", (f"%{keyword}%", f"%{keyword}%"))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="No matching books found")
    return result


# CART ROUTES -----------------------------------------------------------------
@app.post("/cart/add")
def add_to_cart(item: AddToCart):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT copies FROM books WHERE book_id=%s", (item.book_id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if item.qty > book["copies"]:
        raise HTTPException(status_code=400, detail=f"Only {book['copies']} copies available")

    cursor.execute("SELECT qty FROM carts WHERE username=%s AND book_id=%s",
                   (item.username, item.book_id))
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "UPDATE carts SET qty=%s WHERE username=%s AND book_id=%s",
            (item.qty, item.username, item.book_id)
        )
    else:
        cursor.execute(
            "INSERT INTO carts (username, book_id, qty) VALUES (%s,%s,%s)",
            (item.username, item.book_id, item.qty)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Cart updated"}


@app.get("/cart/{username}")
def view_cart(username: str):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT c.book_id, b.name, b.author, b.price, c.qty, (b.price*c.qty) as total
        FROM carts c JOIN books b ON c.book_id=b.book_id
        WHERE c.username=%s
    """, (username,))
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()
    if not cart_items:
        return {"username": username, "cart": [], "total_amount": 0}
    total_amount = sum(item["total"] for item in cart_items)
    return {"username": username, "cart": cart_items, "total_amount": total_amount}


@app.post("/cart/update")
def update_cart(item: AddToCart):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT copies FROM books WHERE book_id=%s", (item.book_id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    cursor.execute("SELECT qty FROM carts WHERE username=%s AND book_id=%s",
                   (item.username, item.book_id))
    existing = cursor.fetchone()

    if not existing:
        raise HTTPException(status_code=404, detail="Item not in cart")

    available = book["copies"] 

    if item.qty > available:
        raise HTTPException(status_code=400, detail=f"Only {available} copies available")

    cursor.execute("UPDATE carts SET qty=%s WHERE username=%s AND book_id=%s",
                   (item.qty, item.username, item.book_id))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Quantity updated"}


@app.post("/cart/clear")
def clear_cart(data: dict):
    username = data.get("username")

    if not username:
        raise HTTPException(status_code=400, detail="Username required")

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM carts WHERE username = %s"
    cursor.execute(query, (username,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Cart cleared."}


# ORDER ROUTES-----------------------------------------------------------------
@app.post("/order/checkout/{username}")
def checkout(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM carts WHERE username=%s", (username,))
    cart_items = cursor.fetchall()
    if not cart_items:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    order_items = []

    for c in cart_items:
        cursor.execute("SELECT * FROM books WHERE book_id=%s", (c["book_id"],))
        book = cursor.fetchone()

        if not book:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail=f"Book ID {c['book_id']} not found")

        if book["copies"] < c["qty"]:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail=f"Not enough copies of {book['name']}")
        total_amount += book["price"] * c["qty"]
        order_items.append({"book_id": c["book_id"], "qty": c["qty"], "price": book["price"]})

    cursor.execute("INSERT INTO orders (username, total_amount) VALUES (%s,%s)", (username, total_amount))
    order_id = cursor.lastrowid

    for item in order_items:
        cursor.execute("INSERT INTO order_items (order_id, book_id, qty, price) VALUES (%s,%s,%s,%s)",
                       (order_id, item["book_id"], item["qty"], item["price"]))
        cursor.execute("UPDATE books SET copies=copies-%s WHERE book_id=%s", (item["qty"], item["book_id"]))

    cursor.execute("DELETE FROM carts WHERE username=%s", (username,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Order placed successfully", "order_id": order_id, "total_amount": round(total_amount, 2)}


@app.get("/orders/{username}")
def get_orders(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE username=%s", (username,))
    orders_list = cursor.fetchall()
    result = []
    for o in orders_list:
        cursor.execute("SELECT * FROM order_items WHERE order_id=%s", (o["order_id"],))
        items = cursor.fetchall()
        result.append({"order_id": o["order_id"], "total_amount": o["total_amount"], "items": items})
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="No orders found")
    return {"orders": result}