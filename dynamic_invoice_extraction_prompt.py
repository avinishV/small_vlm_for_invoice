import json
from typing import List

# Load schema for field descriptions
def load_schema(schema_path: str) -> dict:
    with open(schema_path, 'r') as f:
        return json.load(f)

def get_system_prompt() -> str:
    """
    Returns a system prompt for a VLM/LLM to act as an expert invoice information extractor.
    """
    return (
        "You are an expert document understanding AI specialized in extracting structured data from invoice images. "
        "Your task is to accurately extract all required fields from the provided invoice image, following the field definitions and instructions. "
        "Be precise, robust to layout variations, and handle missing or ambiguous fields gracefully. "
        "Return the extracted data as a JSON object with the specified keys."
    )

def get_invoice_extraction_prompt(fields: List[str], schema_path: str) -> str:
    """
    Returns a user prompt for extracting all fields from an invoice image, using field descriptions from the schema.
    Args:
        fields: List of field names to extract.
        schema_path: Path to the schema JSON file with field descriptions.
    """
    schema = load_schema(schema_path)
    prompt_lines = [
        "Extract the following fields from the invoice image. For each field, follow the extraction instructions:",
        ""
    ]
    for field in fields:
        desc = schema.get(field, {}).get("description", "")
        prompt_lines.append(f"- {field}: {desc}")
    prompt_lines.append("")
    prompt_lines.append(
        "Instructions:\n"
        "1. Carefully read the invoice image and locate each field as described above.\n"
        "2. If a field is missing or not present, return an empty string for that field.\n"
        "3. For item fields (e.g., item_1_description, item_2_quantity), extract the information for each item in the order they appear in the invoice.\n"
        "4. Output the result as a single JSON object with the exact field names as keys.\n"
        "5. Do not include any extra commentary or explanation. Only return the JSON object.\n"
        "6. Be robust to different invoice layouts, fonts, and languages.\n"
        "7. If a field is ambiguous, use your best judgment and note the ambiguity in the value.\n"
        "8. For numberic values, extract only the numeric part (e.g., 809.62) and preserve the original formatting for decimals and thousand separators if present (e.g., 1,234.56 or 809,62)"
        "9. Double-check that all required fields are present in your output."
    )
    return "\n".join(prompt_lines)
