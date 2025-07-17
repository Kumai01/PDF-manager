import argparse
from pathlib import Path

from .__version__ import __version__
from .merge import PDFMergerManager
from .order import PDFOrderManager
from .cut import PDFCutterManager, cut_file
from .gui import run_gui

def main():
    parser = argparse.ArgumentParser(prog="pdfm"
                                     , description="pdf Manager"
                                     , epilog="")
    # args.command
    parser.add_argument("--version", action="version", version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(dest="command")

    gui_parser = subparsers.add_parser("gui")

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("files", nargs="+", help="PDF files to merge")
    merge_parser.add_argument("-o", "--output", help="Ouput PDF file")

    order_parser = subparsers.add_parser("order")
    order_parser.add_argument("file", help="PDF file to order")
    order_parser.add_argument("pages", nargs="+", help="All pages that comes last or after a page")
    order_parser.add_argument("--after", help="The page that pages come after")
    order_parser.add_argument("-o", "--output", help="Ouput PDF file")

    cut_parser = subparsers.add_parser("cut")
    cut_parser.add_argument("file", help="PDF file to cut")
    cut_parser.add_argument("pages", nargs="+", help="Pages to cut")
    cut_parser.add_argument("-o", "--output", help="Ouput PDF file")

    args = parser.parse_args()
    if args.command == "merge":
        merge_args(args.files, args.output)
    elif args.command == "order":
        order_args(args.file, args.pages, args.after, args.output)
    elif args.command == "cut":
        cut_args(args.file, args.pages, args.output)
    elif args.command == "gui":
        run_gui()
    else:
        interactive_mode()

def merge_args(files, output):
    merger = PDFMergerManager()
    for file in files:
        file = validate_pdf_path(file)
        merger.add_file(file)
    final_path = merger.write_output(output)
    print("file is in ", Path(final_path))

def order_args(file, pages, before, output):
    file = validate_pdf_path(file)
    order = PDFOrderManager(file)
    order.order_pages([int(c) for c in pages], int(before))
    final_path = order.write_output(output)
    print("file is in: ", Path(final_path))

def cut_args(file, pages, output):
    file = validate_pdf_path(file)
    cutter = PDFCutterManager(file)
    cutter.cut(pages)
    cutter.write_output(output)

def interactive_mode():
    while True:
            cs = input("choose => merge - order - cut - exit: ").strip()
            match cs:
                case "merge":
                    interactive_merge()
                case "order":
                    interactive_order()
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

def validate_suffix(file: str, suffix: str) -> str : # suffix should sth. like: '.pdf' or '.jpg'
    p = Path(file)
    if p.suffix.lower() != suffix:
        p = p.with_suffix(suffix)
    return str(p)

def validate_file_path(file):
    if not Path(file).exists():
        exit(f"File not Found \nPath of the file: {Path(file).resolve()} \nPath of the current directory: {Path.cwd()}")
    return file

def validate_pdf_path(file: str) -> str:
    file = validate_suffix(file, ".pdf")
    file = validate_file_path()
    return file

def validate_img_path(file: str) -> str:
    file = validate_suffix(file, ".jpg") # TODO it should autmotically check the suffix instead of adding .jpg 
    file = validate_file_path()

def validate_file_path_interactive():
    while True:
        path = input("Give the path to the main file: ").strip()
        if Path(path).exists():
            return path
        else:
            print(f"file: {path} not found\n Please try again.")

if __name__ == "__main__":
    main()

