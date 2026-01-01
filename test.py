# file_path = r"D:\Programs\python\internship\chats\Rupali_Rutuja.txt"

# # Open the file and read line by line
# with open(file_path, 'r') as f:
#     for line in f:
#         print(line)
#         line = line.strip()           # remove leading/trailing whitespace
#         print(line)
#         words = line.split()          # split line into words
#         print(words)
#         for word in words:
#             print(f"{word}\t1")      # emit word and count


# print("Hi \"Python\"")
# print("Hi 'Python'")
# print('Hi \'Python\'')
# print('Hi "Python"')

# print("Your Learning Path:\n\t- Python Basics\n\t- Data Engineering\n\t- AI")
# print("""\nYour Learning Path:
#       - Python Basics
#       - Data Engineering
#       - AI 
# """)

# number = "+49 (176) 123-4567"
# re_number = number.replace("+", "00").replace("(", "").replace(")", ""). replace(" ", "").replace("-", "")
# print(re_number)

# string = "968-Maria, (D@t@ Engineer );; 27y  "
# replaced = string.replace("@", "a").replace("(", "").replace(")", "").replace("968-", "").replace(";; ","").replace(",","").replace("y", "")
# cleaned = replaced.lower().strip()
# print(cleaned)
# print(f"name: {cleaned[:5]} | role: {cleaned[6:-3]} | age: {cleaned[-2:]}")


s = "968-Maria, (D@t@ Engineer );; 27y  "

# Remove extra spaces
s = s.strip()

# Extract name
name = s.split("-")[1].split(",")[0].lower()
print(name)

# Extract role and clean symbols
role = s.split("(")[1].split(")")[0]
role = role.replace("@", "a").strip().lower()
print(role)

# Extract age
age = s.split(";;")[1].strip()
print(age)
age = age.replace("y", "")
print(age)
print(f"name: {name} | role: {role} | age: {age}")
