import timeclass 
MyClass:
    def __init__(self):
        self.data = []
def main():
    objects = []
    while True:
        obj = MyClass()
        obj.data.append(list(range(1000000)))  # Append a large list        objects.append(obj)
        print("aaaa")
        time.sleep(1)

if __name__ == "__main__":
    main()