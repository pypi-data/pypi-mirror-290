from .summarizer import BedrockSummarizer
from .structredExtraction import BedrockstructredExtraction
import os
from loguru import logger

_instance = None


def get_instance(aws_access_key_id=None, aws_secret_access_key=None):
    global _instance
    if _instance is None:
        _instance = BedrockSummarizer(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    return _instance

def get_instance_extraction(aws_access_key_id=None, aws_secret_access_key=None):
    global _instance
    if _instance is None:
        _instance = BedrockstructredExtraction(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    return _instance


def summarize(input_content, user_prompt=None, model_name=None, aws_access_key_id=None, aws_secret_access_key=None):
    """
    Summarizes the given input content. The input can be text, a local file path, or an S3 file path.

    Parameters:
    input_content (str): The content to be summarized. This can be a text string, a local file path, or an S3 file path.
    user_prompt (str, optional): A custom prompt to be used for the summarization. If not provided, a default prompt will be used.
    model_name (str, optional): The name of the model to be used. If not provided, the default model will be used.
    aws_access_key_id (str, optional): AWS Access Key ID.
    aws_secret_access_key (str, optional): AWS Secret Access Key.

    Returns:
    tuple: A tuple containing the summary text, input token count, output token count, and the cost of the operation.
    """
    instance = get_instance(aws_access_key_id, aws_secret_access_key)
    try:
        if os.path.exists(input_content):  # Check if input is a local file path
            return instance.summarize_file(input_content, user_prompt, model_name)
        elif input_content.startswith('s3://'):  # Check if input is an S3 file path
            return instance.summarize_s3_file(input_content, user_prompt, model_name)
        else:  # Assume input is text
            return instance.summarize_text(input_content, user_prompt, model_name)
    except Exception as e:
        user_friendly_error = instance._get_user_friendly_error(e)
        logger.error(user_friendly_error)
        return None, 0, 0, 0.0


def structredExtraction(input_content, user_prompt=None, model_name=None, aws_access_key_id=None, aws_secret_access_key=None):
    """
    Extract the given input content. The input can be text, a local file path, or an S3 file path.

    Parameters:
    input_content (str): The content to be used for extraction. This can be a text string, a local file path, or an S3 file path.
    user_prompt (str, optional): A custom prompt to be used for the Extraction. If not provided, a default prompt will be used.
    model_name (str, optional): The name of the model to be used. If not provided, the default model will be used.
    aws_access_key_id (str, optional): AWS Access Key ID.
    aws_secret_access_key (str, optional): AWS Secret Access Key.

    Returns:
    tuple: A tuple containing the Extracted entity, input token count, output token count, and the cost of the operation.
    """
    instance = get_instance_extraction(aws_access_key_id, aws_secret_access_key)
    try:
        if os.path.exists(input_content):  # Check if input is a local file path
            return instance.extract_file(input_content, user_prompt, model_name)
        elif input_content.startswith('s3://'):  # Check if input is an S3 file path
            return instance.extract_s3_file(input_content, user_prompt, model_name)
        else:  # Assume input is text
            return instance.extract_text(input_content, user_prompt, model_name)
    except Exception as e:
        user_friendly_error = instance._get_user_friendly_error(e)
        logger.error(user_friendly_error)
        return None, 0, 0, 0.0


# article= """"**Apple Camp returns with free sessions for kids aged 6 to 10 years old**

# *By Rich Demuro*

# *(KTLA) -- Apple Camp is back in session, offering free workshops at Apple stores across the country. The theme this year: Exploring new worlds and telling stories inspired by kindness.*

# *""It taught me how to do stuff that I never knew how to do,"" said Grace Kinsera, an Apple Creative Pro.*

# *The free, 90-minute sessions are designed for children ages 6 to 10 years old. They're held throughout the summer.*

# *This particular session focuses on using the iPad to create an interactive storybook.*

# *""They're creating animations, they're adding AR shapes, 3D shapes, taking AR photos where they place the 3D shapes in the world around them,"" said Kinsera.*

# *Kids learn new skills on familiar devices, and sometimes parents do too.*

# *""I'm watching some stuff now that I was like, 'I didn't know that my iPad could do that,'"" said Mili Patel, a parent.*

# *There are bigger lessons as well.*

# *""There's always room for more kindness, and to get these kids thinking about it in a thoughtful, creative way early on is wonderful,"" said Kinsera.*

# *Apple Camp is part of a larger initiative called Today at Apple, which offers free, hands-on sessions that teach valuable skills and hidden tricks.*

# *""We all want our kids to learn about technology, but in a safe way. This is a great opportunity for them to do that,"" said Patel.*

# *Sign-up is open now. Sessions run through the end of July. All campers get a free T-shirt, too!*

# *To sign up, visit apple.com/today.*

# *Copyright 2023 Nexstar Media Inc. All rights reserved. This material may not be published, broadcast, rewritten, or redistributed.*"
# """