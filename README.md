# Invoice Data Extraction

This project is to quickly benchmark VLMs and finetune small VLM for invoice data extraction. The workflow includes dynamic data preparation based on config, prompt generation, and evaluation against ground truth data.

Dataset being used -> https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr  </br>
VLM model to test first -> HuggingFaceTB/SmolVLM-500M-Instruct

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
  
- **LLM Finetuning**:
  - includes code to fine tune Small VLM using HuggingFace Transformer 
      - on single GPU using llm_finetuning/smolvlm-trl-invoice.ipynb script
      - on distrubted GPU using PyTorch accelerate. Refer Readme.md file there. 


## Finetuning results on HuggingFaceTB/SmolVLM-500M-Instruct
1. Finetuned on batch_1/batch_1/batch1_2 invoices and evaluated on batch_1/batch_1/batch1_1 invoices
2. Initial result on full precision model. Refer Kaggle notebook for details - https://www.kaggle.com/code/vermaavi/invoice-data-extraction-using-smolvlm#field-wise-accuracy

    Overall accuracy = 51.8%
    --------field wise-------
    client_name       0.567134
    client_address    0.629259
    seller_name       0.589178
    seller_address    0.641283
    invoice_number    0.993988
    invoice_date      0.997996
    tax               0.000000
    discount          0.000000
    total             0.236473
 
3. Finetuned 8-bit quantised model accuracy. Refer invoice_data_extraction notebook. 
    
    Overall accuracy = 98.7%
    --------field wise-------
    client_name       0.987976
    client_address    0.993988
    seller_name       0.989980
    seller_address    0.989980
    invoice_number    0.985972
    invoice_date      0.997996
    tax               0.971944
    discount          0.997996
    total             0.949900

## How to Run

1. **Prepare Data**:
   Run `prepare_invoice_data.py` to dynamically select fields and generate `prepared_invoice_data.csv`.

2. **Generate Prompts**:
   Use `dynamic_invoice_extraction_prompt.py` to create prompts for the VLM model.

3. **Evaluate Results**:
   Run `invoice_evaluate_response.py` to benchmark extracted data against ground truth.


