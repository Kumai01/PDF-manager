from typing import List, Dict, Optional, Union, Callable, Any
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk # For themed widgets

from pdfm.merge import PDFMergerManager

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
        order_tab: ttk.Frame = ttk.Frame(self.notebook, width=400, height=280)
        self.notebook.add(order_tab, text="Order")

    def choose_file(self) -> str :
        file_path: str = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
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
        messagebox.showinfo("Success", f"Files are merged in: {final_path}")
        files = []
        self.listbox.delete(0, tk.END)


class Tab(ttk.Frame):
    def __init__(self, parent: tk.Tk|ttk.Frame):
        super().__init__(parent, width=400, height=280)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        
        for col in range(3):
            self.columnconfigure(col, weight=1)

    def create_listbox(self, row:int = 1) -> tk.Listbox:
        listbox: tk.Listbox = tk.Listbox(self)
        listbox.grid(row=row, column=0, columnspan=3, sticky="nsew")
        return listbox

    def create_wide_button(self, text: str, command: Callable, row: int) -> None:
        ttk.Button(self, text=text, command=command).grid(row=row, column=0, sticky="wne", columnspan=3)
        return


if __name__ == "__main__":
    run_gui()