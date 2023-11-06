from dataclasses import dataclass
import json
from typing import Any, Dict

@dataclass
class JsonExtraction:
    json_dict: Dict[str, Any]
    response_json_removed: str


def extract_json_from_response(response: str, json_doc_keyword: str) -> JsonExtraction:
    """
    This function extracts a JSON document from a response string.

    Parameters:
    response (str): The response string containing the JSON document.
    json_doc_keyword (str): The keyword indicating the start of the JSON document.

    Returns:
    JsonExtraction: A dataclass containing the extracted JSON document and the remaining response string.
    """
    
    if json_doc_keyword.lower() in response.lower():
        keyword_start = response.lower().index(json_doc_keyword.lower())
        json_doc_start = keyword_start  + len(json_doc_keyword)
        json_str = response[json_doc_start:].strip()

        # check if json is wrapped in markdown-style code block  ```{ "attribute": "value"}  ```
        if (json_str.startswith('```') 
            and json_str.endswith('```')
            and "\n" in json_str):
            # Remove the markdown-style code block, including code language indicator (```json)
            json_str = json_str[json_str.index("\n"):-3].strip()

        response_json_removed = response[:keyword_start].strip()
        print(f'json_doc:\n{json_str}')

        # Load the JSON string into a Python dictionary
        json_dict = json.loads(json_str)
        return json_dict, response_json_removed
    

    return None

