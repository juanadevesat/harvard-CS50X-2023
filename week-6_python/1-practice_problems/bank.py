greeting = input("Greeting: ").lower().strip().split()

if greeting[0][0:5] == "hello":
    print("$0")
elif greeting[0][0] == "h":
    print("$20")
else:
    print("$100")