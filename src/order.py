from PyPDF2 import PdfReader as r
from PyPDF2 import PdfWriter as w
from pathlib import Path

from utils import write_output

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class PDFOrderManager:
    def __init__(self, main_file):
        self.main_file = main_file
        self.reader = r(main_file)
        self.writer = None

    def num_pages(self):
        return len(self.reader.pages)

    def order_pages(self, pages_together, before = None):
        if before is None:
            before = self.num_pages() - 1
        new_order = []
        for i in range(1, self.num_pages() + 1):
            if i in pages_together:
                continue

            new_order.append(i)
            
            if i == before:
                new_order.extend(pages_together)

        self.writer = w()
        for i in new_order:
            self.writer.add_page(self.reader.pages[i - 1])

    def write_output(self, output_name = None):
        if self.writer is None:
            raise ValueError("No ordered pages to write. Call order_pages first.")
        return write_output(self.writer, output_name, self.main_file)

        
if __name__ == "__main__":
    from cli import interactive_order
    interactive_order()

def order_window():
    pass