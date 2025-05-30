import sys
from PyPDF2 import PdfReader as r
from PyPDF2 import PdfWriter as w
from PyPDF2 import PdfMerger as m

if __name__ == "__main__":
    print("starting the program ...")
    file1_name = input("give the full path to the first file: \n")  
    file1 = r(file1_name)
    file2_name = input("give the full path to the second file: \n")  
    file2 = r(file2_name)
    print(f"I read {len(file1.pages)}")
    merge = m()
    merge.append(fileobj=file1)
    merge.append(fileobj=file2)
    merge.write("output.pdf")

