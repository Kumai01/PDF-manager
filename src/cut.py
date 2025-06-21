from PyPDF2 import PdfReader as r
from PyPDF2 import PdfWriter as w
from utils import write_output

class PDFCutterManager:
    def __init__(self, file):
        self.reader = r(file)
        self.writer = w()
        self.main_file = file
        
    def cut(self, cut_pages):
        for i, page in enumerate(self.reader.pages):
            if i != cut_pages:
                self.writer.add_page(page)
    
    def write_output(self, output_name = None):
        if self.writer is None:
            raise ValueError("No ordered pages to write. Call order_pages first.")
        return write_output(self.writer, output_name, self.main_file)

def cut_file(file, cut_pages):
    reader = r(file)
    writer = w()
    for i, page in enumerate(reader.pages):
        if i != cut_pages:
            writer.add_page(page)
    
    with open("output.pdf", "wb") as f:
        writer.write(f)