from BFPCode.BF import bfc

if __name__ == "__main__":
    code = input("BF> ")
    c = bfc(code)
    while True:
        code = input("BF> ")
        if code == "exit":
            break
        if code == "reset":
            c = bfc(code)
        if code == "print":
            print(c)
        c = bfc(code, c)