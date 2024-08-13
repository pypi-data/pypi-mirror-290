import os

import requests

from langchain_openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import ConsoleCallbackHandler

__all__ = [
    'generate_transformation_code'
]
def access_openai():
    """
    Access the OpenAI API using the API key from environment variables.

    Returns:
    - OpenAI: Instance of the OpenAI class.

    Raises:
    - ValueError: If the OPENAI_API_KEY is not found in environment variables.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    llm = ChatOpenAI(api_key=api_key, model_name='gpt-4o-mini')
    return llm

def access_perplexity():
    """
    Access the Perplexity API using the API key from environment variables.

    Returns:
    - function: A function to make requests to the Perplexity API.

    Raises:
    - ValueError: If the PPLX_API_KEY is not found in environment variables.
    """
    api_key = os.getenv('PPLX_API_KEY')
    if not api_key:
        raise ValueError("PPLX_API_KEY not found in environment variables")

    def call_perplexity(model, messages):
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    return call_perplexity

def generate_transformation_code(context,
                                 transformation,
                                 code_template,
                                 use_perplexity=False):
    """
    Generate a Python class definition for transforming data.

    Parameters:
    - context (str): Text providing details of the input data
    - transformation (str): Description of the transformation.
    - use_perplexity (bool): Whether to use Perplexity API instead of OpenAI.

    Returns:
    - str: Class definition as a string.
    """

    if use_perplexity:
        call_perplexity = access_perplexity()
        model = "pplx-7b-online"  # Example model name
        messages = [
            {"role": "system", "content": "Generate a Python code snippet."},
            {"role": "user", "content": f"{context}.\nThe transformation to apply is: {transformation}.\n\nApply the code snippet to this code template and format the code generated: \n{template}"}
        ]
        response = call_perplexity(model, messages)
        code_snippet = response['choices'][0]['message']['content']
    else:
        template=(
            "Generate a Python code snippet that transforms a DataFrame.\n"
            "Context for the transform is as follows.\n{context}. \n"
            "The transformation to apply is: {transformation}. \n"
            "Update the following code template with the columns and code snippet and format the output: {code_template}\n"
            "Format the code using pep8 including docstrings. Provide only final output python code with no explanation."
        )
        llm = access_openai()
        prompt = PromptTemplate(
            input_variables=["code_template"],
            template=template,
            partial_variables={
                "context": context,
                "transformation": transformation
            }
        )
        chain = prompt | llm | StrOutputParser()
        code_snippet = chain.invoke(
            input={
                "code_template": code_template,
            },

            # Debugging
            #config={
            #    'callbacks': [ConsoleCallbackHandler()]
            #}
        )

    # Cleanup
    if '```python' in code_snippet:
        code_snippet = code_snippet.replace("```python","").replace("```","").strip()

    return code_snippet
