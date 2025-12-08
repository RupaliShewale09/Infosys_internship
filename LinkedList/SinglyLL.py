class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    # Create Initial Linked List----------------------------------------
    def accept(self):
        print("\nCreating a linked list =>")
        n = int(input("\nHow many nodes you want to enter initially? "))
        for i in range(n):
            data = int(input(f"Enter data for node {i+1}: "))
            newnode = Node(data)

            if self.head is None:                 # if head is not present (at start i=0)
                self.head = newnode
            else:                                  # when head is present
                temp = self.head
                while temp.next:
                    temp = temp.next
                temp.next = newnode
        self.display()

    # INSERT OPERATIONS----------------------------------------------------
    def insert_begin(self):
        data = int(input("\nEnter data to insert at beginning: "))
        newnode = Node(data)
        newnode.next = self.head
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

        print("Inserted at end")
        self.display()

    def insert_position(self):
        pos = int(input("\nEnter position: "))
        data = int(input("Enter data: "))
        newnode = Node(data)

        if pos <= 0:         # position can't be negative
            print("Invalid position!!!")
            return
 
        if pos == 1:         # postion is head pos
            self.insert_begin()
            return

        temp = self.head
        count = 1            # counts position

        while temp and count < pos - 1:
            temp = temp.next
            count += 1

        if temp is None:
            print("Position out of range!!!")
            return

        newnode.next = temp.next
        temp.next = newnode
        print(f"Inserted at position {pos}")
        self.display()


    # DELETE OPERATIONS----------------------------------------------------
    def delete_begin(self):
        if self.head is None:
            print("List empty!!!")
            return

        self.head = self.head.next
        print("Deleted from beginning")
        self.display()

    def delete_end(self):
        if self.head is None:
            print("List empty!!!")
            return

        if self.head.next is None:
            self.head = None
            print("Last node deleted")
            self.display()
            return

        temp = self.head
        while temp.next.next:
            temp = temp.next
        temp.next = None
        
        print("Deleted from end")
        self.display()

    def delete_position(self):
        if self.head is None:
            print("List empty!!!")
            return
        
        pos = int(input("\nEnter position to delete: "))

        if pos <= 0:
            print("Invalid position!!!")
            return

        if pos == 1:
            self.delete_begin()
            return

        temp = self.head
        count = 1

        while temp and count < pos - 1:
            temp = temp.next
            count += 1

        if temp is None or temp.next is None:
            print("Position out of range!!!")
            return

        temp.next = temp.next.next
        print(f"Deleted node at position {pos}")
        self.display()


    def delete_by_value(self):
        pos = self.search()  # Use your search() function to get position

        if pos is None:
            return

        if pos == 1:
            self.delete_begin()
        else:
            temp = self.head
            for _ in range(pos - 2):
                temp = temp.next
            temp.next = temp.next.next
            
        print(f"\nNode deleted")
        self.display()

    # SEARCH ----------------------------------------------------------
    def search(self):
        key = int(input("\nEnter value : "))
        temp = self.head
        pos = 1
        while temp:
            if temp.data == key:
                print(f"Value {key} found at position {pos}")
                return pos
            temp = temp.next
            pos += 1
        print(f"Value {key} not found!!!")
        return None


    # REVERSE------------------------------------------------------------
    def reverse(self):
        prev = None
        curr = self.head

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        self.head = prev
        print("List reversed")
        self.display()

    # UPDATE--------------------------------------------------------------
    def update(self):
        old = int(input("\nEnter old value to update: "))
        new = int(input("Enter new value: "))

        temp = self.head
        while temp:
            if temp.data == old:
                temp.data = new
                print("Value updated")
                self.display()
                return
            temp = temp.next

        print("Value not found!!!")

    # SORT-----------------------------------------------------------------
    def sort(self, asc=True):
        if self.head is None:
            print("List empty!!!")
            return

        p = self.head
        while p:
            q = p.next
            while q:
                if asc:
                    if p.data > q.data:
                        p.data, q.data = q.data, p.data
                else:  # descending
                    if p.data < q.data:
                        p.data, q.data = q.data, p.data
                q = q.next
            p = p.next

        order = "ascending" if asc else "descending"
        print(f"List sorted in {order} order")
        self.display()

        
    # DISPLAY--------------------------------------------------------------
    def display(self):
        if self.head is None:
            print("List empty!")
            return

        print("\nLinked List: ", end="")
        temp = self.head

        while temp:
            print(f"[ {temp.data} ]", end="")
            if temp.next:
                print(" -> ", end="")
            temp = temp.next

        print(" -> NULL")



# MAIN PROGRAM 
if __name__ == "__main__":
    obj = SinglyLinkedList()
    obj.accept()

    while True:
        print("\n=========== MAIN MENU ===========")
        print("1. Insert")
        print("2. Delete")
        print("3. Search")
        print("4. Reverse")
        print("5. Update")
        print("6. Sort")
        print("7. Display")
        print("8. Exit")

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

            case 3: obj.search()
            case 4: obj.reverse()
            case 5: obj.update()
            case 6:
                while True:
                    print("\n--- SORT MENU ---")
                    print("1. Ascending")
                    print("2. Descending")
                    print("3. Back")
                    sub = int(input("Enter choice: "))

                    match sub:
                        case 1: obj.sort(asc=True)
                        case 2: obj.sort(asc=False)
                        case 3: break  
                        case _: print("Invalid option.")

            case 7: obj.display()
            case 8:
                print("Exiting...")
                break
            case _:
                print("Invalid choice.")
