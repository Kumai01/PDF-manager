import tkinter as tk
from tkinter import ttk # For themed widgets
from .merge import merge_window
from .order import order_window

def run_gui():
    root = tk.Tk()
    root.title("PDF Manager")

    mainframe = ttk.Frame(root, padding="10")
    mainframe.pack(fill=tk.BOTH, expand=True)

    ttk.Button(mainframe, text="Merge PDFs", command=merge_window).pack(pady=10)
    ttk.Button(mainframe, text="Order PDF Pages", command=order_window).pack(pady=10)
    ttk.Button(mainframe, text="Quit", command=root.quit).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()