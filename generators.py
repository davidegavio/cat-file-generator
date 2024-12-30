from pathlib import Path

from reportlab.lib import utils
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def _generate_txt(file_path: Path, file_content: str):
    '''
    Generates a text file with the given content.

    Args:
        file_path (Path): The path where the text file will be created.
        file_content (str): The content to be written to the text file.
    '''
    with open(file_path, 'w') as f:
        f.write(file_content)
        
        
def _generate_pdf(file_path: Path, file_content: str):
    '''
    Generates a PDF file with the given content.
    
    Args:
        file_path (Path): The path where the PDF file will be saved.
        file_content (str): The content to be written into the PDF file.
        
    Returns:
        None
    '''
    
    # Create a Canvas object for the PDF and set the page size to A4
    c = canvas.Canvas(file_path.as_posix(), pagesize=A4)
    
    # Define margins (2.5 cm on all sides) in centimeters
    left_margin = 2.5 * cm
    right_margin = 2.5 * cm
    top_margin = 2.5 * cm
    bottom_margin = 2.5 * cm
    
    # Get the dimensions of an A4 page
    page_width, page_height = A4
    
    # Calculate the usable width (total width minus left and right margins)
    usable_width = page_width - left_margin - right_margin
    
    # Set the initial text position (top left, respecting the top margin)
    text_x = left_margin
    text_y = page_height - top_margin
    
    # Create a TextObject to manage the text, set the origin and font
    text_object = c.beginText()
    text_object.setTextOrigin(text_x, text_y)
    text_object.setFont('Times-Roman', 12)  # Font 'Times-Roman' with size 12 pt
    
    # Use simpleSplit to split the text content into lines
    # The text is split to fit within the usable width
    lines = utils.simpleSplit(file_content, 'Times-Roman', 12, usable_width)
    
    # Iterate over each line produced by simpleSplit
    for line in lines:
        # Add the line to the TextObject
        text_object.textLine(line)
        
        # Update the vertical position (y) to move to the next line
        text_y -= 14  # 12 pt font height + 2 pt line spacing
        
        # If the text reaches the bottom margin, create a new page
        if text_y < bottom_margin:
            # Finalize the current page
            c.showPage()
            
            # Reset the vertical position for the new page
            text_y = page_height - top_margin
            
            # Create a new TextObject for the new page and reset settings
            text_object = c.beginText()
            text_object.setTextOrigin(text_x, text_y)
            text_object.setFont('Times-Roman', 12)  # Reset the font for the new page
    
    # Draw the TextObject on the Canvas, rendering all the text
    c.drawText(text_object)
    
    # Save the PDF file
    c.save()