from typing import List
import img2pdf

def convert(imgs: List[str], output: str = "output") -> str:
    with open(f"pdfm_output/{output}.pdf", "wb") as f:
        f.write(img2pdf.convert(imgs))
    # accepts: .jpg, .jpeg, .png, .bmp, .gif, .tif, .tiff, .webp, .ico, .ppm, .pgm, .pdf, .eps

if __name__ == "__main__":
    pass