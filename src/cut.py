from PyPDF2 import PdfReader as r
from PyPDF2 import PdfWriter as w
from pathlib import Path

def cut_file(file, cut_pages):
    reader = r(file)
    writer = w()
    for i, page in enumerate(reader.pages):
        if i != cut_pages:
            writer.add_page(page)
    
    with open("output.pdf", "wb") as f:
        writer.write(f)