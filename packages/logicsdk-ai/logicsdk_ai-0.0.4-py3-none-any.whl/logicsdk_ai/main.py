from .summarizer import BedrockSummarizer
import os
from loguru import logger

_instance = None


def get_instance(aws_access_key_id=None, aws_secret_access_key=None):
    global _instance
    if _instance is None:
        _instance = BedrockSummarizer(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
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