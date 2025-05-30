from PyPDF2 import PdfReader as r
from PyPDF2 import PdfWriter as w
from pathlib import Path

def run_order():
    main_path = input("give the path to the main file: \n")  
    main_file = r(main_path)
    num_pages = len(main_file.pages)

    pages = []
    while True:
        page = input("Enter page number (or 'done' to finish): ").strip()
        if page.lower() == "done" :
            break
        
        try:
            if int(page) > num_pages:
                raise ValueError
            pages.append(int(page) - 1)
        except ValueError:
            print("Please enter a valid number or 'done' to finish.")
    
    try:
        before = int(input("Enter after what page you want to put the pages: ").strip()) - 1
        if before > num_pages or before in pages:
            raise ValueError
    except ValueError:
        print("Please enter a valid page that is not in the moved pages")
        
    new_order = []
    for i in range(num_pages):
        if i in pages:
            continue

        new_order.append(i)
        
        if i == before:
            new_order.extend(pages)

    result = w()
    for i in new_order:
        result.add_page(main_file.pages[i])
    
    Path("output").mkdir(exist_ok=True)
    result.write(Path("output") / Path(main_path).name)

        
if __name__ == "__main__":
    run_order()