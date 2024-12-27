import json
from datetime import datetime
from io import StringIO
from pathlib import Path

from cat.mad_hatter.decorators import hook, tool
from cat.utils import get_static_path
from fastapi.responses import FileResponse, StreamingResponse

from .generator_engine import handle_generation


@tool
def request_handler(tool_input, cat):
    '''
        Generate a file with the specified content and extension.
        Generate also a message with the download link.
        User may say:
        - "Generate a [file_extension] file with the content: [content]"
        - "Generate a [file_extension] file containing: [content]"
        - "Can you create a [file_extension] file with this text: [content]?"
        - "Please generate a [file_extension] file with the following text: [content]"
        - "Make a [file_extension] file with this content: [content]"
        - "Create a [file_extension] file with this content: [content]"
    '''
    
    json_llm_prompt = '''
        Extract two keywords from the following text and create a dictionary with those keywords as keys and their corresponding values from the input text.
        For example, in the text: 'Generate a [file_extension] file with the content: [content]',
        the dictionary should look like:
        {
            'file_extension': '[file_extension]',
            'content': '[content]'
        }

        Now, process the following text and return a dictionary with the extracted keywords and their corresponding values:
    ''' + tool_input
    
    json_request = json.loads(cat.llm(json_llm_prompt))
    html_message = handle_generation(file_name='file', file_extension=json_request['file_extension'], file_content=json_request['content'])
    for message in html_message:
        cat.send_chat_message(message)