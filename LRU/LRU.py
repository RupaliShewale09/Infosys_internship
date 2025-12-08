from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()   # key → value

    def get(self, key):
        if key not in self.cache:
            return -1

        # move key to end - MRU
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        # if key exists, update and move to end
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
            return

        # if full, remove least recently used (first item)
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)   

        # insert new pair as most recent
        self.cache[key] = value

    def display(self):
        if not self.cache:
            print("Cache is empty")
            return

        print("\nLRU Cache (Least → Most Recent):")
        for k, v in self.cache.items():
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
