import json
import re

from cat.log import log
from cat.mad_hatter.decorators import tool

from .generator_engine import handle_generation
from .utils import examples


@tool(return_direct=True, examples=examples
)
def generate_file(tool_input, cat):
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
    ''' + f'\n\n {tool_input}'
    
    cat.send_notification('Preprocessing the input text...')
    raw_content = cat.llm(json_llm_prompt)
    log.info("Raw content from LLM:" + raw_content)

    cleaned_content = re.sub(r'```json|```', '', raw_content)
    cleaned_content = re.sub(r'^.*?{', '{', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'}.*$', '}', cleaned_content, flags=re.DOTALL)

    log.info("Cleaned content: " + cleaned_content)

    try:
        json_request = json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        cat.send_error('JSON decode error, please contact the plugin developer for assistance.')
        log.info("JSON decode error:" + str(e))
    
    cat.send_notification('Generating the file...')
    html_message = handle_generation(file_name='file', file_extension=json_request['file_extension'], file_content=json_request['content'])
    
    for message in html_message:
        cat.send_chat_message(message)
        
    if html_message:
        return 'File generated successfully!'
    else:
        return 'File not generated!'