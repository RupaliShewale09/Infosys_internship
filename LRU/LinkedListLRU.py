# Node class for doubly linked list
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

# LRU Cache using Doubly Linked List
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.head = None  # LRU side
        self.tail = None  # MRU side

    # Move node to MRU position 
    def _move_to_end(self, node):
        if node == self.tail:
            return  # already MRU
        # remove node
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next  # node was head
        if node.next:
            node.next.prev = node.prev
        # add to tail
        node.prev = self.tail
        node.next = None
        if self.tail:
            self.tail.next = node
        self.tail = node
        if not self.head:
            self.head = node

    # GET operation
    def get(self, key):
        current = self.head
        while current:
            if current.key == key:
                self._move_to_end(current)
                return current.value
            current = current.next
        return -1

    # PUT operation
    def put(self, key, value):
        current = self.head
        while current:
            if current.key == key:
                current.value = value
                self._move_to_end(current)
                return
            current = current.next
        # if key not found, insert new
        new_node = Node(key, value)
        if self.size < self.capacity:
            if not self.head:
                self.head = self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            self.size += 1
        else:
            # remove LRU node (head)
            lru = self.head
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            # insert new node at tail
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    # DISPLAY nodes from LRU → MRU
    def display_nodes(self):
        if not self.head:
            print("ERROR: Cache is empty")
            return
        print("\nLRU Cache Nodes (Least → Most Recent):")
        current = self.head
        while current:
            print(f"[{current.key}:{current.value}]", end="")
            if current.next:
                print(" -> ", end="")
            current = current.next
        print("\n")


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    print("\n============ LRU Program (Linked List Only) ============\n")
    size = int(input("Enter LRU Cache Size: "))
    lru = LRUCache(size)

    while True:
        print("\n----- LRU MENU -----")
        print("1. PUT key value")
        print("2. GET key")
        print("3. DISPLAY cache nodes")
        print("4. EXIT")

        choice = int(input("\nEnter choice: "))

        match(choice):
            case 1:
                key = input("\nEnter key: ")
                value = input("Enter value: ")
                lru.put(key, value)
                print("Inserted")
                lru.display_nodes()

            case 2:
                key = input("\nEnter key to get: ")
                val = lru.get(key)
                if val == -1:
                    print("ERROR: Key not found!!!")
                else:
                    print("Value:", val)
                lru.display_nodes()

            case 3:
                lru.display_nodes()

            case 4:
                print("Exiting...")
                break

            case _:
                print("Invalid choice.")
