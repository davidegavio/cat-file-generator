from pathlib import Path

from cat.utils import get_static_path

from .generators import _generate_pdf, _generate_txt
from .utils import _generate_html_message


def handle_generation(file_name: str, file_extension: str, file_content: str):
    """
    Handles the generation of a file with the specified name, extension, and content.
    Args:
        file_name (str): The name of the file to be generated.
        file_extension (str): The extension of the file to be generated (e.g., 'txt', 'pdf').
        file_content (str): The content to be written into the file.
    Returns:
        str: An HTML message indicating the result of the file generation.
    Raises:
        ValueError: If the provided file extension is not supported.
    """
    
    directory = Path(get_static_path()) / 'generated_files'

    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / f'{file_name}.{file_extension}'
    
    if file_path.exists():
        file_path.unlink()  # Remove the file if it already exists
        
    if file_extension == 'txt':
        _generate_txt(file_path=file_path, file_content=file_content)
    elif file_extension == 'pdf':
        _generate_pdf(file_path=file_path, file_content=file_content)
    else:
        raise ValueError("Unsupported file extension")
    
    html_message = _generate_html_message(file_name, file_extension, file_path)
    
    return html_message

