import json
import os
import re
from tabulate import tabulate

FILE = "students.json"   # JSON file to store student records


# Load & Save Functions (File Handling)
def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_data(students):
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)


students = load_data()


# Validation Functions
def validate_name(name):
    return re.fullmatch(r"[A-Za-z ]{3,30}", name) is not None

def validate_dept(dept):
    return re.fullmatch(r"[A-Za-z]{2,10}", dept) is not None

def validate_mobile(mobile):
    return re.fullmatch(r"[0-9]{10}", mobile) is not None

def validate_year(year):
    return year.isdigit() and 1 <= int(year) <= 4


# Auto-increment Register Number
def get_next_reg():
    if not students:
        return "1001"
    last = max(int(s["reg"]) for s in students)
    return str(last + 1)

# Utility: Safe Input with Loop
def input_loop(prompt, validation_func, error_message):
    """Keeps asking until valid"""
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print(error_message)

# CRUD Operations -------------------------------------------------------------

# 1. Add Student
def add_student():
    print("\n--- Add New Student ---")
    reg = get_next_reg()
    print(f"Assigned Register Number: {reg}")

    name = input_loop("Enter Name: ",
                        validate_name,
                        "❌ Invalid! Name must contain letters only (3–30 chars).")

    dept = input_loop("Enter Department: ",
                        validate_dept,
                        "❌ Invalid! Department must be 2–10 alphabets.")

    year = input_loop("Enter Year (1-4): ",
                        validate_year,
                        "❌ Invalid! Year must be between 1 and 4.")

    mobile = input_loop("Enter Mobile Number (10 digits): ",
                        validate_mobile,
                        "❌ Invalid! Mobile must be exactly 10 digits.")

    student = {
        "reg": reg,
        "name": name,
        "dept": dept,
        "year": year,
        "mobile": mobile
    }

    students.append(student)
    save_data(students)
    print("✔️ Student added successfully!")


# 2. View all students
def view_students():
    print("\n--- All Student Records ---")

    if not students:
        print("No records found!")
        return

    table = []
    for s in students:
        table.append([s["reg"], s["name"], s["dept"], s["year"], s["mobile"]])

    print(tabulate(table,
                   headers=["Reg No", "Name", "Dept", "Year", "Mobile"],
                   tablefmt="fancy_grid"))


# 3. Search Student
def search_student():
    print("\n--- Search Student ---")
    print("1. Search by Register Number")
    print("2. Search by Name")
    choice = input("Enter choice: ")

    results = []

    if choice == "1":
        reg = input("Enter Register Number: ")
        for s in students:
            if s["reg"] == reg:
                results.append(s)

    elif choice == "2":
        name = input("Enter Name: ").lower()
        for s in students:
            if name in s["name"].lower():
                results.append(s)
    else:
        print("Invalid option!")
        return

    if not results:
        print("❌ No matching student found!")
        return

    table = []
    for s in results:
        table.append([s["reg"], s["name"], s["dept"], s["year"], s["mobile"]])

    print("\n✔ Matching Records:\n")
    print(tabulate(table,
                   headers=["Reg No", "Name", "Dept", "Year", "Mobile"],
                   tablefmt="fancy_grid"))

# 4. Update Student
def update_student():
    print("\n--- Update Student ---")
    reg = input("Enter Register Number: ")

    for s in students:
        if s["reg"] == reg:
            print("\nRecord Found! Type NA or leave blank to Skip updating.")

            # ----- NAME -----
            new_name = input("New Name: ")
            if new_name.strip() != "" and new_name.lower() != "na":
                if validate_name(new_name):
                    s["name"] = new_name
                else:
                    print("❌ Invalid Name! Skipped.")

            # ----- DEPT -----
            new_dept = input("New Department: ")
            if new_dept.strip() != "" and new_dept.lower() != "na":
                if validate_dept(new_dept):
                    s["dept"] = new_dept
                else:
                    print("❌ Invalid Department! Skipped.")

            # ----- YEAR -----
            new_year = input("New Year (1-4): ")
            if new_year.strip() != "" and new_year.lower() != "na":
                if validate_year(new_year):
                    s["year"] = new_year
                else:
                    print("❌ Invalid Year! Skipped.")

            # ----- MOBILE -----
            new_mobile = input("New Mobile (10 digits): ")
            if new_mobile.strip() != "" and new_mobile.lower() != "na":
                if validate_mobile(new_mobile):
                    s["mobile"] = new_mobile
                else:
                    print("❌ Invalid Mobile! Skipped.")

            save_data(students)
            print("✔️ Record updated successfully!")
            return

    print("❌ Student not found!")


# 5. Delete Student
def delete_student():
    print("\n--- Delete Student ---")
    reg = input("Enter Register Number: ")

    for s in students:
        if s["reg"] == reg:
            students.remove(s)
            save_data(students)
            print("✔️ Record deleted successfully!")
            return

    print("❌ Student not found!")



# MAIN MENU
while True:
        print("\n==================================")
        print(" STUDENT RECORD MANAGEMENT SYSTEM")
        print("====================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = int(input("\nEnter choice: "))

        match(choice):
            case 1:
                add_student()
            case 2:
                view_students()
            case 3:
                search_student()
            case 4:
                update_student()
            case 5:
                delete_student()
            case 6:
                print("Exiting...")
                break
            case _:
                print("❌ Invalid choice!")

