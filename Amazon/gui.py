import tkinter as tk
from tkinter import messagebox
from main import get_amazon_product


def check_availability():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter an Amazon URL!")
        return

    output_box.delete("1.0", tk.END)

    try:
        data = get_amazon_product(url)
        output_box.insert(tk.END,
                          f"Title       : {data['name']}\n"
                          f"Price       : {data['price']}\n"
                          f"Availability: {data['availability']}\n")
    except Exception as e:
        output_box.insert(tk.END, f"⚠️ Error fetching product:\n{e}")

def clear_input():
    url_entry.delete(0, tk.END) 
    output_box.delete("1.0", tk.END)  


# ---------------------------------
root = tk.Tk()
root.title("Amazon Availability Checker")
root.geometry("500x450")   # square window
root.resizable(False, False)
root.configure(bg= 'white' ,highlightthickness=15, highlightcolor="#D19BFF")

# ---------------------------------
heading = tk.Label(
    root,
    text="Amazon Product Availability",
    font=("Cambria", 20, "bold"),
    bg='white'
)
heading.pack(pady=20)

url_label = tk.Label(
    root,
    text="Enter Amazon URL:",
    font=("Cambria", 13),
    bg='white'
)
url_label.pack(anchor="w", padx=20)


# ---------------------------------------
url_entry = tk.Entry(
    root,
    width= 55,
    font=("Cambria", 12),
    bd=1
)
url_entry.pack(padx=20, pady=7)


# ---------------------------------------
button_frame = tk.Frame(root, bg='white')
button_frame.pack(pady=20)

# Check button
check_btn = tk.Button(
    button_frame,
    text="Check",
    font=('Cambria', 14, 'bold'),
    bg="#E78FB7", 
    fg="white", 
    width=13,
    command=check_availability
)
check_btn.pack(side=tk.LEFT, padx=10) 

# Clear button
clear_button = tk.Button(
    button_frame, 
    text="Clear", 
    bg='white',
    font=('Cambria', 10),
    command=clear_input
)
clear_button.pack(side=tk.LEFT, padx=10)


# ----------------------------------------
output_label = tk.Label(
    root,
    text="Product Information:",
    font=("Cambria", 14, "bold"),
    bg='white'
)
output_label.pack(anchor="w", padx=20)

output_box = tk.Text(
    root,
    width=55,
    height=10,
    font=("Cambria", 11)
)
output_box.pack(padx=20, pady=5)

root.mainloop()
