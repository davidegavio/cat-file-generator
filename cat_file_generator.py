import json
import re

from cat.log import log
from cat.mad_hatter.decorators import tool

from .generator_engine import handle_generation


@tool(return_direct=True, examples = [
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
        "Create a pdf file with this content: 'The PDF file contains an extensive discussion of the topic at hand. The content is thorough, spanning several paragraphs, and covers a wide range of subtopics. It includes technical details, historical context, and various methodologies used in the process. This document is aimed at providing a full understanding of the topic for anyone who reads it.'"
    ]
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