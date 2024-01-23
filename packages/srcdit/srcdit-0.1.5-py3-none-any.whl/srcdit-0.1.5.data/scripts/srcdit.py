#!python
import sys


def key_value_edit(file, key_value):
    key, value = key_value.split("=")

    try:
        int(value)
    except ValueError:
        value = f'"{value}"'

    with open(file, "r") as f:
        data = f.read()
        lines = data.split("\n")
        for i in range(len(lines)):
            if lines[i].find(key) != -1:
                print("Found line with given key")
                lines[i] = f"{key}={value}"
                break
        else:
            print("Key not found.")
            while True:
                yes_no = input("Add new? (y/n)\n")
                if yes_no.lower() in ["yes", "y"]:
                    lines.append(f"{key}={value}")
                    break
                elif yes_no.lower() in ["no", "n"]:
                    print("Not written")
                    return
                else:
                    print("Invalid input. Please enter yes/no")
    with open(file, "w") as f:
        data = "\n".join(lines)
        f.write(data)
        print("Written out")


def main():
    if len(sys.argv) != 3:
        print("Invalid arguments")
        return
    key_value_edit(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
