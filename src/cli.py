import argparse
from merge import PDFMergerManager
from order import *
from cut import cut_file
from utils import 

def main():
    parser = argparse.ArgumentParser(prog="pdfm"
                                     , description="pdf Manager"
                                     , epilog="")
    # args.command
    subparsers = parser.add_subparsers(dest="command")

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("files", nargs="+", help="PDF files to merge")
    merge_parser.add_argument("-o", "--output", help="Ouput PDF file")

    order_parser = subparsers.add_parser("order")
    order_parser.add_argument("file", help="PDF file to order")
    order_parser.add_argument("pages", nargs="+", help="All pages that comes last or after a page")
    order_parser.add_argument("--after", help="The page that pages come after")
    args = parser.parse_args()
    if args.command == "merge":
        merge_args(args.files, args.output)
    elif args.command == "order":
        order_args(args.pages, args.after)
    else:
        interactive_mode()

def merge_args(files, output):
    merger = PDFMergerManager()
    for file in files:
        merger.add_file(file)
    print("file is in ./", merger.write_output(output))

def order_args(file, pages, before):
    order = PDFOrderManager(file)
    order.order_pages(pages, before)

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

    merger.add_file(validate_file_path())

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
    order = PDFOrderManager(validate_file_path())
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
    path = validate_file_path()
    cut_pages = int(input("Enter pages to cut: "))
    cut_file(path, cut_pages)

def validate_file_path():
    while True:
        path = input("Give the path to the main file: ").strip()
        if Path(path).exists():
            return path
        else:
            print(f"file: {path} not found\n Please try again.")

if __name__ == "__main__":
    main()

