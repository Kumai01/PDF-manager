import argparse
from merge import PDFMergerManager
from order import *
from cut import cut_file

def main():
    parser = argparse.ArgumentParser(prog="pdfm"
                                     , description="pdf Manager"
                                     , epilog="")
    # args.command
    subparsers = parser.add_subparsers(dest="command")

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("files", nargs="+", help="PDF files to merge")
    merge_parser.add_argument("-o", "--output", required=True, help="Ouput PDF file")

    args = parser.parse_args()
    if args.command == "merge":
        merge_parser.print_help
    else:
        interactive_mode()

def interactive_mode():
    while True:
            cs = input("choose => merge - order - cut - exit: ").strip()
            match cs:
                case "merge":
                    interactive_merge()
                case "order":
                    run_order_cli()
                case "cut":
                    interactive_cut()
                case "exit":
                    print("Exiting program.")
                    break
                case _:
                    print("try again")
                    continue

def interactive_merge():
    merger = PDFMergerManager()
    while True:
        main_path = input("Give the path to the main file: ").strip()
        try:
            merger.add_file(main_path)
            break
        except Exception as e:
            print(f"Error: {e}\nPlease try again.")

    try:
        n = int(input("# of files you want to merge: "))
    except ValueError:
        print("Please enter a valid number.")
    i = 0
    while i < n:
        try:
            merger.add_file(input(f"file {i+1}: "))
            i += 1
        except FileNotFoundError:
            print("File not found, try again.")
    print("output is in: ", merger.write_output())
    
def interactive_order():
    main_path = input("give the path to the main file: \n")  
    order = PDFOrderManager(main_path)
    num_pages = order.num_pages()

    pages = []
    while True:
        page = int(input("Enter page number (or '-1' to finish): ").strip())
        if page == -1 :
            break
        try:
            if page > num_pages:
                raise ValueError
            pages.append(int(page) - 1)
        except ValueError:
            print("Please enter a valid number or '-1' to finish.")
    
    try:
        before = int(input("Enter after what page you want to put the pages: ").strip()) - 1
        if before > num_pages or before in pages:
            raise ValueError
    except ValueError:
        print("Please enter a valid page that is not in the moved pages")

    order.order_pages(pages, before)    
    
    print("output is in: ", order.write_output())


def interactive_cut():
    file_name = input("Enter file name: ")
    cut_pages = int(input("Enter pages to cut: "))
    cut_file(file_name, cut_pages)
    
if __name__ == "__main__":
    main()

