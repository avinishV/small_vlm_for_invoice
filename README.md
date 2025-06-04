# Invoice Data Extraction Workflow

This project is to quickly benchmark VLMs (small and finetuned one). The workflow includes dynamic data preparation based on config, prompt generation, and evaluation against ground truth data.

Dataset being used -> 
VLM model to test first -> 

## File Structure

- **Dynamic Data Preparation**:
  - `prepare_invoice_data.py`: Script for preparing data.
  - `data/batch1_1.csv`: Original CSV file.
  - `data/prepared_invoice_data.csv`: Output file with dynamically selected fields.

- **Dynamic Prompt Creation**:
  - `dynamic_invoice_extraction_prompt.py`: Script for generating prompts.
  - `configs/invoice_schema.json`: Schema file with field descriptions.

- **Evaluation**:
  - `invoice_evaluate_response.py`: Script for evaluating extracted data.
  - `configs/invoice_eval_config.yaml`: Configuration file for evaluation rules.

## How to Run

1. **Prepare Data**:
   Run `prepare_invoice_data.py` to dynamically select fields and generate `prepared_invoice_data.csv`.

2. **Generate Prompts**:
   Use `dynamic_invoice_extraction_prompt.py` to create prompts for the VLM model.

3. **Evaluate Results**:
   Run `invoice_evaluate_response.py` to benchmark extracted data against ground truth.


