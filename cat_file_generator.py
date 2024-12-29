import json

from cat.log import log
from cat.mad_hatter.decorators import tool

from .generator_engine import handle_generation


@tool
def generate_file(tool_input, cat, return_direct=True):
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
        For example, in the text: "Generate a [file_extension] file with the content: [content]",
        the dictionary should look like:
        {
            "file_extension": "[file_extension]",
            "content": "[content]"
        }

        Now, process the following text and return a dictionary with the extracted keywords and their corresponding values:
        
    ''' + tool_input
        
    json_request = json.loads(cat.llm(json_llm_prompt))
    
    content = json_request['content'].replace('"', '', 1)
    content = json_request['content'][::-1].replace('"', '', 1)[::-1]
    html_message = handle_generation(file_name='file', file_extension=json_request['file_extension'], file_content=content)
    
    for message in html_message:
        cat.send_chat_message(message)
        
    if html_message:
        return 'File generated successfully!'
    else:
        return 'File not generated!'