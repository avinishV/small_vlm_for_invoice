"""
json schema for invoice evaluation response.
{
  "client_name": "",
  "client_address": "",
  "seller_name": "",
  "seller_address": "",
  "invoice_number": "",
  "invoice_date": "",
  "tax": "",
  "discount": "",
  "total": ""
}
"""

import pandas as pd
import yaml
import json
from rapidfuzz import fuzz
from typing import Dict
import importlib.util

def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['fields']

def extract_invoice_fields(json_str):
    """
    Extracts required fields from the invoice JSON string.
    Returns a flat dict with the required keys.
    """
    if isinstance(json_str, float):  # Handle NaN
        return {k: "" for k in [
            "client_name", "client_address", "seller_name", "seller_address",
            "invoice_number", "invoice_date", "tax", "discount", "total"
        ]}
    try:
        data = json.loads(json_str)
    except Exception:
        data = eval(json_str)  # fallback if not strict JSON

    invoice = data.get("invoice", {})
    subtotal = data.get("subtotal", {})

    return {
        "client_name": invoice.get("client_name", ""),
        "client_address": invoice.get("client_address", ""),
        "seller_name": invoice.get("seller_name", ""),
        "seller_address": invoice.get("seller_address", ""),
        "invoice_number": invoice.get("invoice_number", ""),
        "invoice_date": invoice.get("invoice_date", ""),
        "tax": subtotal.get("tax", ""),
        "discount": subtotal.get("discount", ""),
        "total": subtotal.get("total", ""),
    }

def match_field(gt, pred, match_type, threshold=100):
    if pd.isna(gt) and pd.isna(pred):
        return True
    if match_type == 'exact':
        return str(gt).strip() == str(pred).strip()
    elif match_type == 'fuzzy':
        score = fuzz.ratio(str(gt), str(pred))
        return score >= threshold
    elif match_type == 'partial_fuzzy':
        score = fuzz.partial_ratio(str(gt), str(pred))
        return score >= threshold
    else:
        raise ValueError(f"Unknown match_type: {match_type}")

def evaluate(ground_df, output_df, config):
    results = []
    total, correct = 0, 0

    for idx, row in ground_df.iterrows():
        file_name = row['invoice_no'] if 'invoice_no' in row else row['File Name']
        gt_json = json.loads(row['requested_data']) if isinstance(row['requested_data'], str) else row['requested_data']
        pred_json = json.loads(output_df.loc[output_df['invoice_no'] == file_name, 'response'].values[0])
        requested_fields = json.loads(row['requested_parameters']) if isinstance(row['requested_parameters'], str) else row['requested_parameters']
        row_result = {'invoice_no': file_name}
        for field in requested_fields:
            rule = config[field]
            gt_val = gt_json.get(field, "")
            pred_val = pred_json.get(field, "")
            matched = match_field(gt_val, pred_val, rule['match_type'], rule.get('threshold', 100))
            row_result[field] = int(matched)
            total += 1
            correct += int(matched)
        results.append(row_result)
    accuracy = correct / total if total else 0
    return pd.DataFrame(results), accuracy

if __name__ == "__main__":
    # Paths
    ground_path = "./data/prepared_invoice_data.csv"
    config_path = "./configs/invoice_eval_config.yaml"

    # Load data
    ground_df = pd.read_csv(ground_path)
    config = load_config(config_path)

    print("Ground Truth Data:")
    print(ground_df.head())

    # Load vlm model response  data
    output_path = "./data/vlm_response.csv"
    output_df = pd.read_csv(output_path)

    # Evaluate
    results_df, accuracy = evaluate(ground_df, output_df, config)
    print(f"Overall Accuracy: {accuracy:.4f}")
    results_df.to_csv("fieldwise_eval_results.csv", index=False)
    print("Fieldwise results saved to fieldwise_eval_results.csv")
