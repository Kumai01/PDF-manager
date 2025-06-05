from PyPDF2 import PdfWriter as w
from pathlib import Path

def write_output(writer, output_name, first_file):
        Path("output").mkdir(exist_ok=True)
        if output_name is None:
            if first_file:
                output_name = Path(first_file).name
            else:
                # this case should not happen
                output_name = "merged.pdf"

        output_path = Path("output") / output_name
        writer.write(output_path)
        writer.close()
        return output_path