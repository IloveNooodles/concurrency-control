import argparse

# parser = argparse.ArgumentParser(
#   description="Concurrency Control Protocl Implementation"
# )


if __name__ == "__main__":
    filename = "test/tc1.txt"
    file = open(filename, "r")
    arr = file.read()
    arr = arr.split(";")