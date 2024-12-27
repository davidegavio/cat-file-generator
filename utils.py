import os


def _generate_html_message(file_name, file_extension, file_path):
    """
    Generates an HTML message with a download link for a file.

    Args:
        file_name (str): The name of the file without extension.
        file_extension (str): The extension of the file.
        file_path (str): The path to the file.

    Returns:
        str: An HTML string containing a download link for the specified file.
    """
    file_size = os.path.getsize(file_path)
    file_size_kb = file_size / 1024
    
    file_info_html = [
        f'<p><strong>File Name:</strong> {file_name}</p>',
        f'<p><strong>File Size:</strong> {file_size_kb:.2f} KB</p>',
        f'<p><a href="/static/generated_files/{file_name}.{file_extension}" download="{file_name}.{file_extension}">Download</a></p>'
    ]
    return file_info_html