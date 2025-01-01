import os

from langchain_text_splitters import RecursiveCharacterTextSplitter


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

examples = [
    "Generate a txt file with the content: 'Sample text.'",
    "Generate a pdf file with the content: 'PDF content.'",
    "Generate a txt file containing: 'Short text content.'",
    "Generate a pdf file containing: 'Short PDF content.'",
    "Can you create a txt file with this text: 'Hello, world.'?",
    "Can you create a pdf file with this text: 'PDF example.'?",
    "Please generate a txt file with the following text: 'This is an example of a text file with moderate length.'",
    "Please generate a pdf file with the following text: 'This PDF file contains a sentence of moderate length.'",
    "Make a txt file with this content: 'Here is an example of a medium-sized .txt file content.'",
    "Make a pdf file with this content: 'Here is a PDF file with medium-length content.'",
    "Create a txt file with this content: 'This text file contains a few more words than a shorter example.'",
    "Create a pdf file with this content: 'The content in this PDF is a bit longer than the shorter versions.'",
    "Generate a txt file with the content: 'This text file contains a more detailed explanation of the task at hand. It includes multiple sentences that describe what needs to be done in a step-by-step manner.'",
    "Generate a pdf file with the content: 'This is an extended example of a PDF file. It contains more detailed information, including multiple ideas and examples that provide better understanding of the task.'",
    "Please generate a txt file with the following text: 'The contents of this text file describe how to perform a specific task. The steps are outlined clearly, with additional explanations and notes for better clarity.'",
    "Please generate a pdf file with the following text: 'The PDF content here provides detailed insights on how to use certain functions. It covers multiple aspects of the process and ensures the reader understands the key points.'",
    "Create a txt file with this content: 'This text file contains a very detailed and lengthy explanation of a complex process. The content spans multiple paragraphs, each of which delves into various aspects of the topic. It discusses the history, methodology, and expected outcomes in great detail, providing the reader with comprehensive knowledge.'",
    "Create a pdf file with this content: 'The PDF file contains an extensive discussion of the topic at hand. The content is thorough, spanning several paragraphs, and covers a wide range of subtopics. It includes technical details, historical context, and various methodologies used in the process. This document is aimed at providing a full understanding of the topic for anyone who reads it.'",
    "Generate a markdown (.md) file with the content: '# Sample Title\\nThis is a simple Markdown file.'",
    "Generate a markdown (.md) file with the following content: '# Introduction\\nThis is an example of a Markdown file with headings, lists, and links.'",
    "Can you create a markdown file with this content: '## List of Items\\n- Item 1\\n- Item 2\\n- Item 3.'",
    "Please generate a markdown file with the following content: '### Code Example\\n```python\\ndef hello():\\n    print(\\'Hello, world!\\')\\n```.'",
    "Make a markdown (.md) file with this content: '# Header\\nThis Markdown file contains **bold text**, *italic text*, and [links](https://example.com).'",
    "Create a markdown file with this content: '## Markdown Example\\nThis file contains a mix of **bold text**, inline code (`print()`), and a block of code.'",
    "Generate a markdown file with the content: 'This Markdown file includes a table:\\n\\n| Header 1 | Header 2 |\\n|---------|---------|\\n| Row 1   | Data 1  |\\n| Row 2   | Data 2  |.'",
    "Create a markdown file with the content: '## Complex Markdown Example\\nThis Markdown file contains lists, code blocks, and inline code:\\n- Item 1\\n- Item 2\\n\\n```python\\n# Example code block\\ndef example():\\n    return True\\n```.'"
]
