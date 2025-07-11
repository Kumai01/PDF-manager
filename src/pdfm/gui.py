import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk # For themed widgets

from pdfm.merge import PDFMergerManager

def run_gui():
    root = Application()
    root.mainloop() # so that the window doesn't close immediately


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("PDF Manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.create_home_tab()
        self.create_merge_tab()
        self.create_order_tab()

    def create_home_tab(self):
        home_tab = ttk.Frame(self.notebook, width=400, height=280)
        self.notebook.add(home_tab, text="Home")
    
    def create_merge_tab(self):
        merge_tab = ttk.Frame(self.notebook, width=400, height=280)
        self.notebook.add(merge_tab, text="Merge")
        
        for col in range(3):
            merge_tab.columnconfigure(col, weight=1)

        listbox = tk.Listbox(merge_tab)
        listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
        

        files = []
        ttk.Button(merge_tab, text="Choose File", command=lambda : self.choose_files(listbox, files)).grid(row=0, column=0, sticky="wne", columnspan=3)
    
        ttk.Button(merge_tab, text="Merge files", command=lambda : self.merge(files)).grid(row=2, column=0, sticky="wne", columnspan=3)

    
    def create_order_tab(self):
        order_tab = ttk.Frame(self.notebook, width=400, height=280)
        self.notebook.add(order_tab, text="Order")

    def choose_files(self, listbox, files: list):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            files.append
            listbox.insert(tk.END, file_path)

    def merge(self, files):
        merger = PDFMergerManager()
        for file in files:
            merger.add_file(file)
        final_path = merger.write_output()
        messagebox.showinfo("Success", f"Files are merged in: {final_path}!")


class Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0)
        ttk.Label(self, text="thatWorked").grid(row=0, column=0)


if __name__ == "__main__":
    run_gui()