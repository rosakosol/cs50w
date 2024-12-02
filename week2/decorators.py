def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done!")
    return wrapper

@announce
def hello():
    print("Hello World!")


hello()
