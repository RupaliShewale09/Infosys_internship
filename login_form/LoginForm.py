import tkinter as tk
from tkinter import messagebox
import login_form.db as db
import login_form.registration_form as registration_form   


def main():
    global root, username, password, show_password
    show_password = False

    root = tk.Tk()
    root.title("Login Form")
    root.geometry("400x400")
    root.configure(bg='white', highlightthickness=20, highlightcolor="#D19BFF")

    # TITLE
    tk.Label(root, text="LOGIN FORM", font=("Cambria", 20, "bold"), bg="white").pack(pady=20)

    # USERNAME
    tk.Label(root, text="Username:", font=("Cambria", 12), bg="white").place(x=30, y=100)
    username = tk.Entry(root, width=30, bd=0)
    username.place(x=130, y=100)
    tk.Frame(root, height=2, width=180, bg="#FF5DA2").place(x=130, y=122)

    # PASSWORD
    tk.Label(root, text="Password:", font=("Cambria", 12), bg="white").place(x=30, y=170)
    password = tk.Entry(root, width=30, show="*", bd=0)
    password.place(x=130, y=170)
    tk.Frame(root, height=2, width=180, bg="#FF5DA2").place(x=130, y=192)

    # FUNCTIONS
    def toggle_password():
        global show_password
        if show_password:
            password.config(show="*")
            show_password = False
        else:
            password.config(show="")
            show_password = True

    def login():
        user = username.get()
        pwd = password.get()

        if user == "" or pwd == "":
            messagebox.showwarning("Warning", "Fields cannot be empty!")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Login Success", "Welcome, " + user + "!")
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

        username.delete(0, tk.END)
        password.delete(0, tk.END)
        username.focus_set()

    # SHOW PASSWORD CHECKBOX
    tk.Checkbutton(root, text="show password", font=("Cambria", 12),
                   bg="white", command=toggle_password).place(x=200, y=200)

    # LOGIN BUTTON
    tk.Button(root, text="Login", width=12, font=("Cambria", 14),
              bg='#FF5DA2', command=login).place(x=130, y=240)

    # REGISTER LINK
    def open_signup():
        root.destroy()
        registration_form.main()

    tk.Label(root, text="New User?", bg="white", font=("Cambria", 11)).place(x=110, y=300)
    reg = tk.Label(root, text="Register", fg="blue", bg="white",
                   cursor="hand2", font=("Cambria", 11, "underline"))
    reg.place(x=190, y=300)
    reg.bind("<Button-1>", lambda e: open_signup())

    root.mainloop()


if __name__ == "__main__":
    main()
