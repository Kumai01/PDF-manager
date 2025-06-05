from PyPDF2 import PdfReader as r
from PyPDF2 import PdfWriter as w
from pathlib import Path

from utils import write_output
from cli import interactive_order

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class PDFOrderManager:
    def __init__(self, main_file):
        self.main_file = main_file
        self.order = r()

    def num_pages(self):
        return len(self.order.pages)

    def order_pages(self, pages_together, before):
        new_order = []
        for i in range(self.num_pages):
            if i in pages_together:
                continue

            new_order.append(i)
            
            if i == before:
                new_order.extend(pages_together)

        result = w()
        for i in new_order:
            result.add_page(self.main_file.pages[i])

    def write_output(self, output_name = None):
        write_output(self.order, output_name, self.main_file)

        
if __name__ == "__main__":
    interactive_order()

def order_window():
    pass