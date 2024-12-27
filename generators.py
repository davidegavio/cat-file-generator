from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def _generate_txt(file_path: Path, file_content: str):
    """
    Generates a text file with the given content.

    Args:
        file_path (Path): The path where the text file will be created.
        file_content (str): The content to be written to the text file.
    """
    with open(file_path, 'w') as f:
        f.write(file_content)
        
def _generate_pdf(file_path: Path, file_content: str):
    """
    Generates a PDF file with the given content.
    Args:
        file_path (Path): The path where the PDF file will be saved.
        file_content (str): The content to be written into the PDF file.
    Returns:
        None
    """
    c = canvas.Canvas(file_path.as_posix(), pagesize=letter)
    x = 100
    y = 750

    c.drawString(x, y, file_content)
    c.save()