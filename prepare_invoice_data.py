import pandas as pd
import json
import random
import yaml

# Load the original data
input_path = "./data/batch1_1.csv"
df = pd.read_csv(input_path)

# Load fields from YAML config
with open("./configs/invoice_eval_config.yaml", "r") as f:
    fields = yaml.safe_load(f)["fields"]

all_fields = list(fields.keys())
print("all_fields: ", all_fields)

# Helper to extract item fields
def extract_item_fields(items, max_items=5):
    result = {}
    for i in range(max_items):
        idx = i + 1
        if i < len(items):
            item = items[i]
            result[f"item_{idx}_description"] = item.get("description", "")
            result[f"item_{idx}_quantity"] = item.get("quantity", "")
            result[f"item_{idx}_total_price"] = item.get("total_price", "")
        else:
            result[f"item_{idx}_description"] = ""
            result[f"item_{idx}_quantity"] = ""
            result[f"item_{idx}_total_price"] = ""
    return result

rows = []
for idx, row in df.iterrows():
    json_data = row['Json Data']
    try:
        data = json.loads(json_data)
    except Exception:
        data = eval(json_data)
    invoice = data.get("invoice", {})
    subtotal = data.get("subtotal", {})
    items = data.get("items", [])
    # Build flat dict only for fields present in config
    flat = {}
    for field in all_fields:
        if field.startswith("item_"):
            # Parse item fields like item_1_description, item_2_quantity, etc.
            parts = field.split("_")
            if len(parts) == 3 and parts[0] == "item":
                idx = int(parts[1]) - 1
                key = parts[2]
                if idx < len(items):
                    flat[field] = items[idx].get(key if key != "total_price" else "total_price", "")
                else:
                    flat[field] = ""
            else:
                flat[field] = ""
        else:
            # Header fields
            if field in invoice:
                flat[field] = invoice.get(field, "")
            elif field in subtotal:
                flat[field] = subtotal.get(field, "")
            else:
                flat[field] = ""
                
    # Randomly select 7 to all fields (majority with more fields)
    if random.random() < 0.7:
        n_fields = random.randint(7, len(all_fields))
    else:
        n_fields = random.randint(3, 6)
    requested = sorted(random.sample(all_fields, n_fields))
    requested_data = {k: flat[k] for k in requested}
    rows.append({
        "invoice_no": flat.get("invoice_number", ""),
        "requested_parameters": json.dumps(requested),
        "requested_data": json.dumps(requested_data)
    })

out_df = pd.DataFrame(rows)
out_df.to_csv("./data/prepared_invoice_data.csv", index=False)
print("Saved prepared_invoice_data.csv with dynamic requested fields including item-level fields.")
