from PyPDF2 import PdfMerger as m
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog

from utils import write_output

class PDFMergerManager:
    def __init__(self):
        self.merger = m()
        self.first_file = None

    def add_file(self, file):
        if not self.first_file:
            self.first_file = file
        self.merger.append(file)

    def write_output(self, output_name = None):
        return write_output(self.merger, output_name, self.first_file)

if __name__ == "__main__":
    from cli import interactive_merge
    interactive_merge()

def merge_window():
    win = tk.Toplevel()
    win.title("Merge PDFs")
    selected_files = []