class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []     # list of (key, value) pairs

    def get(self, key):
        # search key
        for i, (k, v) in enumerate(self.cache):
            if k == key:
                # move to end (most recently used)
                self.cache.append(self.cache.pop(i))
                return v
        return -1

    def put(self, key, value):
        # check if key already exists
        for i, (k, v) in enumerate(self.cache):
            if k == key:
                # update + move to end
                self.cache.pop(i)
                self.cache.append((key, value))
                return

        # if new key and cache full, remove LRU (index 0)
        if len(self.cache) >= self.capacity:
            self.cache.pop(0)

        # insert new at end
        self.cache.append((key, value))

    def display(self):
        if not self.cache:
            print("Cache is empty")
            return

        print("\nLRU Cache (Least → Most Recent):")
        for k, v in self.cache:
            print(f"({k}: {v})", end="  ")
        print("\n")

# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    print("\n============ LRU Program ============\n")
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
                lru.display()

            case 2:
                key = input("\nEnter key to get: ")
                val = lru.get(key)
                if val == -1:
                    print("ERROR: Key not found!!!")
                else:
                    print("Value:", val)
                lru.display()

            case 3:
                lru.display()

            case 4:
                print("Exiting...")
                break

            case _:
                print("Invalid choice.")
