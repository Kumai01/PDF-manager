from PyPDF2 import PdfWriter as w
from pathlib import Path

def write_output(writer, output_name: str | None, first_file: str) -> str:
        Path("pdfm_output").mkdir(exist_ok=True)
        if output_name is None:
            if first_file:
                output_name = Path(first_file).name
            else:
                # this case should not happen
                output_name = "merged.pdf"
        else:
            output_name = write_suffix_if_needed(output_name)              

        output_path = str(Path("pdfm_output").resolve() / output_name)
        writer.write(output_path)
        writer.close()
        return output_path

def write_suffix_if_needed(name: str) -> str:
    if len(name) < 4 or name[-4:] != ".pdf":
        name += ".pdf"
    return name