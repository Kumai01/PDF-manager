from merge import run_merge
from order import run_order
__version__ = "0.0.1"

if __name__ == "__main__":
    while True:
        cs = input("choose => merge - order - exit: ").strip()
        match cs:
            case "merge":
                run_merge()
            case "order":
                run_order()
            case "exit":
                print("Exiting program.")
                break
            case _:
                print("try again")
                continue

