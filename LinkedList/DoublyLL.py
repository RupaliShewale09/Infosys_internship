# ---------------- NODE CLASS ----------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


# ---------------- DOUBLY LINKED LIST CLASS ----------------
class DoublyLinkedList:
    def __init__(self):
        self.head = None

    # -------- CREATE INITIAL LIST --------
    def accept(self):
        print("\nCreating doubly linked list =>")
        n = int(input("How many nodes you want to enter initially? "))

        for i in range(n):
            data = int(input(f"Enter data for node {i+1}: "))
            newnode = Node(data)

            if self.head is None:
                self.head = newnode
            else:
                temp = self.head
                while temp.next:
                    temp = temp.next
                temp.next = newnode
                newnode.prev = temp

        self.display()

    # ---------------- INSERT ----------------
    def insert_begin(self):
        data = int(input("\nEnter data to insert at beginning: "))
        newnode = Node(data)

        if self.head:
            newnode.next = self.head
            self.head.prev = newnode

        self.head = newnode
        print("Inserted at beginning")
        self.display()

    def insert_end(self):
        data = int(input("\nEnter data to insert at end: "))
        newnode = Node(data)

        if self.head is None:
            self.head = newnode
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = newnode
            newnode.prev = temp

        print("Inserted at end")
        self.display()

    def insert_position(self):
        pos = int(input("\nEnter position: "))
        data = int(input("Enter data: "))
        newnode = Node(data)

        if pos <= 0:
            print("Invalid position!")
            return

        if pos == 1:
            self.insert_begin()
            return

        temp = self.head
        count = 1

        while temp and count < pos - 1:
            temp = temp.next
            count += 1

        if temp is None:
            print("Position out of range!")
            return

        newnode.next = temp.next
        newnode.prev = temp

        if temp.next:
            temp.next.prev = newnode

        temp.next = newnode
        print(f"Inserted at position {pos}")
        self.display()

    # ---------------- DELETE ----------------
    def delete_begin(self):
        if self.head is None:
            print("List empty!")
            return

        if self.head.next:
            self.head = self.head.next
            self.head.prev = None
        else:
            self.head = None

        print("Deleted from beginning")
        self.display()

    def delete_end(self):
        if self.head is None:
            print("List empty!")
            return

        temp = self.head

        if temp.next is None:  # only one node
            self.head = None
        else:
            while temp.next:
                temp = temp.next
            temp.prev.next = None

        print("Deleted from end")
        self.display()

    def delete_position(self):
        pos = int(input("\nEnter position to delete: "))

        if pos <= 0:
            print("Invalid position!")
            return

        if self.head is None:
            print("List empty!")
            return

        if pos == 1:
            self.delete_begin()
            return

        temp = self.head
        count = 1

        while temp and count < pos:
            temp = temp.next
            count += 1

        if temp is None:
            print("Position out of range!")
            return

        # adjust links
        if temp.prev:
            temp.prev.next = temp.next
        if temp.next:
            temp.next.prev = temp.prev

        print(f"Node at position {pos} deleted")
        self.display()

    def delete_by_value(self):
        key = int(input("\nEnter value to delete: "))
        temp = self.head

        while temp:
            if temp.data == key:
                if temp.prev:
                    temp.prev.next = temp.next
                else:
                    self.head = temp.next

                if temp.next:
                    temp.next.prev = temp.prev

                print(f"Node {key} deleted")
                self.display()
                return

            temp = temp.next

        print("Value not found!")

    # ---------------- TRAVERSAL ----------------
    def traverse_forward(self):
        print("\nForward: ", end="")
        temp = self.head
        while temp:
            print(f"[ {temp.data} ]", end="")
            if temp.next:
                print(" <-> ", end="")
            temp = temp.next
        print(" -> NULL")

    def traverse_backward(self):
        print("Backward: ", end="")
        temp = self.head
        if temp is None:
            print("List empty!")
            return

        while temp.next:
            temp = temp.next

        while temp:
            print(f"[ {temp.data} ]", end="")
            if temp.prev:
                print(" <-> ", end="")
            temp = temp.prev
        print(" -> NULL")

    # ---------------- DISPLAY ----------------
    def display(self):
        self.traverse_forward()
        self.traverse_backward()


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    obj = DoublyLinkedList()
    obj.accept()

    while True:
        print("\n=========== MAIN MENU ===========")
        print("1. Insert")
        print("2. Delete")
        print("3. Display")
        print("4. Exit")

        ch = int(input("Enter choice: "))

        match ch:
            case 1:
                while True:
                    print("\n--- INSERT MENU ---")
                    print("1. Insert at Begin")
                    print("2. Insert at End")
                    print("3. Insert at Position")
                    print("4. Back")
                    sub = int(input("Enter choice: "))
                    match sub:
                        case 1: obj.insert_begin()
                        case 2: obj.insert_end()
                        case 3: obj.insert_position()
                        case 4: break
                        case _: print("Invalid option.")

            case 2:
                while True:
                    print("\n--- DELETE MENU ---")
                    print("1. Delete Begin")
                    print("2. Delete End")
                    print("3. Delete Position")
                    print("4. Delete by Value")
                    print("5. Back")
                    sub = int(input("Enter choice: "))
                    match sub:
                        case 1: obj.delete_begin()
                        case 2: obj.delete_end()
                        case 3: obj.delete_position()
                        case 4: obj.delete_by_value()
                        case 5: break
                        case _: print("Invalid option.")

            case 3: obj.display()
            case 4:
                print("Exiting...")
                break
            case _:
                print("Invalid choice.")
