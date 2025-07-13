from PyPDF2 import PdfWriter as w
from pathlib import Path

def write_output(writer, output_name, first_file):
        Path("pdfm_output").mkdir(exist_ok=True)
        if output_name is None:
            if first_file:
                output_name = Path(first_file).name
            else:
                # this case should not happen
                output_name = "merged.pdf"
        elif len(output_name) < 4 or output_name[-4:] != ".pdf":
              output_name += ".pdf"

        output_path = Path("pdfm_output").resolve() / output_name
        writer.write(output_path)
        writer.close()
        return output_path