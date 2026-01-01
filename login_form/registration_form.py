import tkinter as tk
from tkinter import messagebox
import pymysql
import db as db
import LoginForm as LoginForm


def main():
    root = tk.Tk()
    root.title("Signup UI")
    root.geometry("500x600")
    root.configure(bg="white", highlightthickness=20, highlightcolor="#D19BFF")

    tk.Label(root, text="Welcome!", font=("Cambria", 26, "bold"), bg="white").pack(pady=(25, 0))

    tk.Label(root, text="Create your new account for Free!!", font=("Cambria", 12), bg="white", fg="gray4").pack(pady=(0, 25))

    # ---------------------- PLACEHOLDER FIELD FUNCTION ---------------------- #
    def create_field(label, placeholder, password=False):
        frame = tk.Frame(root, bg="white")
        
        tk.Label(frame, text=label, font=("Cambria", 12, "bold"), bg="white").pack(anchor="w")

        entry = tk.Entry(frame, font=("Cambria", 12), width=35, fg="gray", bd=0)
        entry.insert(0, placeholder)

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")
                if password:
                    entry.config(show="*")

        def on_focus_out(e):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="gray", show="")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entry.pack()
        tk.Frame(frame, height=2, width=330, bg="#FF5DA2").pack(pady=(0, 15))
        frame.pack()

        return entry

    # ---------------------- FIELDS ---------------------- #
    username = create_field("Username", "Enter your Username")
    email = create_field("Email", "Enter your Email")
    phone = create_field("Phone Number", "Enter your Phone Number")
    password = create_field("Password", "Enter your Password", password=True)

    # ---------------------- SHOW/HIDE PASSWORD ---------------------- #
    show_password = False

    def toggle_password():
        nonlocal show_password
        if show_password:
            password.config(show="*")
            show_password = False
        else:
            password.config(show="")
            show_password = True

    tk.Checkbutton(root, text="Show Password", font=("Cambria", 12), bg="white", command=toggle_password).pack(anchor="e")

    # ---------------------- CLEAR FIELDS ---------------------- #
    def clear_fields():
        username.delete(0, tk.END)
        email.delete(0, tk.END)
        phone.delete(0, tk.END)
        password.delete(0, tk.END)

    # ---------------------- SIGNUP FUNCTION ---------------------- #
    def signup():
        u = username.get().strip()
        e = email.get().strip()
        p = phone.get().strip()
        pwd = password.get().strip()

        if u == "" or e == "" or p == "" or pwd == "":
            messagebox.showwarning("Warning", "All fields are required!")
            clear_fields()
            return

        if len(pwd) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters!")
            clear_fields()
            return

        if not p.isdigit() or len(p) != 10:
            messagebox.showerror("Error", "Phone number must be 10 digits!")
            clear_fields()
            return

        if "@" not in e or "." not in e.split("@")[-1]:
            messagebox.showerror("Error", "Enter a valid email address!")
            clear_fields()
            return

        conn = db.get_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users(username, email, phone, password) VALUES (%s, %s, %s, %s)",
                        (u, e, p, pwd))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")

            root.destroy()
            LoginForm.main()

        except pymysql.err.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
            clear_fields()

        conn.close()

    # ---------------------- SIGN UP BUTTON ---------------------- #
    tk.Button(root, text="Sign Up", font=("Cambria", 14, "bold"), bg="#FF5DA2", fg="white", width=25, command=signup).pack(pady=20)

    # ---------------------- LOGIN LINK ---------------------- #
    tk.Label(root, text="Already have an account?", bg="white", font=("Cambria", 11)).pack()

    login_label = tk.Label(root, text="Log In", fg="blue", bg="white", cursor="hand2", font=("Cambria", 11, "underline"))
    login_label.pack()

    login_label.bind("<Button-1>", lambda e: (root.destroy(), LoginForm.main()))

    root.mainloop()


if __name__ == "__main__":
    main()
