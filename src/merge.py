from PyPDF2 import PdfMerger as m
from pathlib import Path

def run_merge():
    while True:
        main_path = input("Give the path to the main file: ").strip()
        try:
            merge = m()
            merge.append(main_path)
            break
        except Exception as e:
            print(f"Error: {e}\nPlease try again.")

    try:
        n = int(input("# of files you want to merge: "))
    except ValueError:
        print("Please enter a valid number.")
    i = 0
    while i < n:
        try:
            merge.append(input(f"file {i+1}: "))
            i += 1
        except FileNotFoundError:
            print("File not found, try again.")
    
    Path("output").mkdir(exist_ok=True)
    merge.write(Path("output") / Path(main_path).name)

if __name__ == "__main__":
    run_merge()