from typing import List
import img2pdf

from .utils import write_suffix_if_needed

def convert(imgs: List[str], output: str = "output.pdf") -> str:
    output = write_suffix_if_needed(output)
    with open(f"pdfm_output/{output}", "wb") as f:
        f.write(img2pdf.convert(imgs))
    # accepts: .jpg, .jpeg, .png, .bmp, .gif, .tif, .tiff, .webp, .ico, .ppm, .pgm, .pdf, .eps

if __name__ == "__main__":
    pass