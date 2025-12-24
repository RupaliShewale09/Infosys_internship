import os
import tkinter as tk
from tkinter import messagebox

USERS_FILE = r"D:\Programs\python\internship\chatApplication\users.txt"
CHAT_DIR = r"D:\Programs\python\internship\chatApplication\chats"
BG_COLOR = "#f5f7fa"
PRIMARY = "#4a6cf7"
TEXT_COLOR = "#333333"


def load_users():
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, "r") as f:
        for line in f:
            if line.strip():
                username, phone, password = line.strip().split("|")
                users[username] = {"phone": phone, "password": password}
    return users


def save_user(username, phone, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}|{phone}|{password}\n")


def get_chat_file(user1, user2):
    u1, u2 = sorted([user1, user2])
    os.makedirs(CHAT_DIR, exist_ok=True)
    return os.path.join(CHAT_DIR, f"{u1}_{u2}.txt")


def save_message(sender, receiver, message):
    with open(get_chat_file(sender, receiver), "a") as f:
        f.write(f"{sender}: {message}\n")


def load_messages(user1, user2):
    path = get_chat_file(user1, user2)
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()

# -------------------- GUI Application --------------------

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("900x550")
        self.root.configure(bg=BG_COLOR)
        self.username = None
        self.current_chat_user = None
        self.start_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def styled_button(self, parent, text, command, color=PRIMARY):
        return tk.Button(parent, text=text, bg=color, fg="white", activebackground=color, relief="flat", padx=12, pady=6, command=command)

    def start_screen(self):
        self.clear()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Welcome to Chat App", font=("Segoe UI", 20, "bold"), bg=BG_COLOR).pack(pady=20)
        self.styled_button(frame, "Login", self.login_screen).pack(pady=8)
        self.styled_button(frame, "Create Account", self.signup_screen).pack(pady=8)

    # ---------------- Signup ----------------
    def signup_screen(self):
        self.clear()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Create Account", font=("Segoe UI", 18, "bold"), bg=BG_COLOR).pack(pady=10)

        self.su_username = self.input_field(frame, "Username")
        self.su_phone = self.input_field(frame, "Phone (10 digits)")
        self.su_password = self.input_field(frame, "Password", show="*")

        self.styled_button(frame, "Sign Up", self.create_account).pack(pady=12)
        tk.Button(frame, text="Back", command=self.start_screen, relief="flat").pack()

    def input_field(self, parent, label, show=None):
        tk.Label(parent, text=label, bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=5)
        entry = tk.Entry(parent, show=show, width=30)
        entry.pack(pady=4)
        return entry

    def create_account(self):
        username = self.su_username.get().strip()
        phone = self.su_phone.get().strip()
        password = self.su_password.get().strip()

        if not username or not phone or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return

        users = load_users()
        for u in users:
            if u.lower() == username.lower():
                messagebox.showerror("Error", "Username already exists")
                return
        for u in users.values():
            if u["phone"] == phone:
                messagebox.showerror("Error", "Phone already registered")
                return

        save_user(username, phone, password)
        messagebox.showinfo("Success", "Account created successfully")
        self.start_screen()

    # ---------------- Login ----------------
    def login_screen(self):
        self.clear()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Segoe UI", 18, "bold"), bg=BG_COLOR).pack(pady=10)
        self.li_username = self.input_field(frame, "Username")
        self.li_password = self.input_field(frame, "Password", show="*")

        self.styled_button(frame, "Login", self.login).pack(pady=12)
        tk.Button(frame, text="Back", command=self.start_screen, relief="flat").pack()

    def login(self):
        username = self.li_username.get().strip()
        password = self.li_password.get().strip()
        users = load_users()

        if username not in users or users[username]["password"] != password:
            messagebox.showerror("Error", "Invalid credentials")
            return

        self.username = username
        self.main_chat_screen()

    # ---------------- Logout ----------------
    def logout(self):
        self.username = None
        self.current_chat_user = None
        self.start_screen()

    # ---------------- Main Chat Screen ----------------
    def main_chat_screen(self):
        self.clear()
        self.root.configure(bg="white")

        top = tk.Frame(self.root, bg=PRIMARY, height=50)
        top.pack(fill=tk.X)
        tk.Label(top, text=f"Logged in as {self.username}", bg=PRIMARY, fg="white", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=15)
        tk.Button(top, text="Logout", bg="#ff4d4d", fg="white", relief="flat", command=self.logout).pack(side=tk.RIGHT, padx=15, pady=8)

        body = tk.Frame(self.root)
        body.pack(fill=tk.BOTH, expand=True)

        self.users_listbox = tk.Listbox(body, width=25)
        self.users_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.users_listbox.bind("<<ListboxSelect>>", self.select_user)

        right = tk.Frame(body)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.chat_area = tk.Text(right, state=tk.DISABLED)
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        bottom = tk.Frame(right)
        bottom.pack(fill=tk.X)
        self.message_entry = tk.Entry(bottom)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.styled_button(bottom, "Send", self.send).pack(side=tk.RIGHT, padx=5)

        self.load_user_list()
        self.auto_refresh_chat()

    def load_user_list(self):
        self.users_listbox.delete(0, tk.END)
        for user in load_users():
            if user != self.username:
                self.users_listbox.insert(tk.END, user)

    def select_user(self, event):
        if not self.users_listbox.curselection():
            return
        self.current_chat_user = self.users_listbox.get(self.users_listbox.curselection()[0])
        self.refresh_chat()

    def refresh_chat(self):
        if not self.current_chat_user:
            return
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.insert(tk.END, load_messages(self.username, self.current_chat_user))
        self.chat_area.config(state=tk.DISABLED)

    def send(self):
        if not self.current_chat_user:
            messagebox.showerror("Error", "Select a user")
            return
        msg = self.message_entry.get().strip()
        if msg:
            save_message(self.username, self.current_chat_user, msg)
            self.message_entry.delete(0, tk.END)
            self.refresh_chat()

    def auto_refresh_chat(self):
        if self.current_chat_user:
            self.refresh_chat()
        self.root.after(100, self.auto_refresh_chat)  


def launch_new_window():
    new_win = tk.Toplevel(root)
    ChatApp(new_win)

# -------------------- Run --------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Launcher")
    root.geometry("300x200")

    tk.Label( root, text="Chat Application",font=("Segoe UI", 14, "bold")).pack(pady=20)

    tk.Button(root, text="Open New User Window", command=launch_new_window, bg=PRIMARY, fg="white", relief="flat", padx=10, pady=6).pack(pady=10)

    root.mainloop()

