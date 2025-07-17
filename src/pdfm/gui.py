from typing import List, Dict, Optional, Union, Callable, Any
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, StringVar
from tkinter import ttk # For themed widgets

from pdfm.merge import PDFMergerManager
from pdfm.order import PDFOrderManager

def run_gui():
    root: Application = Application()
    root.mainloop() # so that the window doesn't close immediately


class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("700x600")
        self.title("PDF Manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.notebook: ttk.Notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.file_path_var = StringVar(self)
        self.create_home_tab()
        self.create_merge_tab()
        self.create_order_tab()

    def create_home_tab(self) -> None:
        home_tab: ttk.Frame = ttk.Frame(self.notebook, width=400, height=280)
        self.notebook.add(home_tab, text="Home")

        label: ttk.Label = ttk.Label(home_tab, text="Welcome to PDF-Manager", font=("Arial", 12, "bold"))
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def create_merge_tab(self) -> None:
        merge_tab: Tab = Tab(self)
        self.notebook.add(merge_tab, text="Merge")

        files: List[str]= []
        self.listbox: tk.Listbox = merge_tab.create_listbox(row=1)
        merge_tab.create_wide_button(text="Choose Files", command=lambda : self.update_files(files), row=0)
        merge_tab.create_wide_button(text="Merge Files", command=lambda : self.merge(files), row=2)

    def create_order_tab(self) -> None:
        self.order_tab: Tab = Tab(self)
        self.notebook.add(self.order_tab, text="Order")

        self.order_tab.create_wide_button(text="Choose a File", command=self.choose_file_and_order_buttons, row=0)
        self.order_tab.create_label(text=self.file_path_var, row=2)

        self.order_tab.create_wide_button(text="Order", command=self.order, row=3)

    def choose_file_and_order_buttons(self) -> None:
        self.choose_file()
        self.order : PDFMergerManager = PDFOrderManager(self.file_path_var.get())
        ttk.Button(self.order_tab, text="Reorder all pages", command=self.take_pages_all).grid(row=1, column=0, sticky="wne", columnspan=2)
        ttk.Button(self.order_tab, text="Reorder some pages", command=self.take_pages_some).grid(row=1, column=2, sticky="wne", columnspan=2)

    def choose_file(self) -> str :
        file_path: str = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            return file_path

    def update_files(self, files: List[str]) -> None:
        file_path: str = self.choose_file()
        files.append(file_path)
        self.listbox.insert(tk.END, file_path)

    def merge(self, files: List[str]):
        merger: PDFMergerManager = PDFMergerManager()
        for file in files:
            merger.add_file(file)
        final_path: str = merger.write_output()
        files = []
        self.listbox.delete(0, tk.END)

    def order(self) -> None:
        if self.new_order is not None:
            self.order.order_pages(new_order=self.new_order)
            final_path: str = self.order.write_output()
            self.success_message(final_path)
            return
        if self.pages_together is not None and self.after is not None:
            self.order.order_pages(pages_together=self.pages_together, before=self.before)
            final_path: str = self.order.write_output()
            self.success_message(final_path)
            return

    def take_pages_all(self):
        order_str = simpledialog.askstring("Page Order", f"Enter new order (1-{self.order.num_pages()}), comma-separated):")
        ttk.Label(self.order_tab, text=order_str)
        
        self.new_order = [int(i.strip()) - 1 for i in order_str.split(",")]
        if any(i < 0 or i >= self.order.num_pages() for i in self.new_order):
            raise ValueError("Page numbers out of range.")
        

    def take_pages_some(self):
        dialog = TwoFieldDialog(self)
        if dialog.result:
            self.pages_together, self.before = dialog.result
            
    def success_message(self, final_path: str) -> None:
        messagebox.showinfo("Success", f"Files are merged in: {final_path}")

class Tab(ttk.Frame):
    def __init__(self, parent: tk.Tk|ttk.Frame):
        super().__init__(parent, width=400, height=280)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        
        for col in range(4):
            self.columnconfigure(col, weight=1)

    def create_listbox(self, row:int = 1) -> tk.Listbox:
        listbox: tk.Listbox = tk.Listbox(self)
        listbox.grid(row=row, column=0, columnspan=4, sticky="nsew")
        return listbox

    def create_wide_button(self, text: str, command: Callable, row: int) -> None:
        ttk.Button(self, text=text, command=command).grid(row=row, column=0, sticky="wne", columnspan=4)

    def create_label(self, text: str, row: int) -> None:
        ttk.Label(self, textvariable=text).grid(row=row, column=0, sticky="wne", columnspan=4)

class TwoFieldDialog(simpledialog.Dialog):
    def body(self, parent: ttk.Frame):
        tk.Label(parent, text="Pages to drage:").grid(row=0)
        tk.Label(parent, text="Put the pages after:").grid(row=1)

        self.pages_to_move = tk.Entry(parent)
        self.before = tk.Entry(parent)

        self.pages_to_move.grid(row=0, column=1)
        self.before.grid(row=1, column=1)

        return self.pages_to_move  # initial focus

    def apply(self):
        self.result = (self.pages_to_move.get(), self.before.get())

if __name__ == "__main__":
    run_gui()