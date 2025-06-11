This folder includes scripts to finetune Vision Language Model on invoice dataset.

**Fine-Tuning Method Summary**</br>
**Base Model**</br>
We fine-tune the pretrained HuggingFaceTB/SmolVLM-500M-Instruct multimodal LLM.

**8-bit Quantization (BitsAndBytesConfig)**</br>
The model weights are quantized to 8-bit precision to slash memory usage while preserving computation throughput.

**PEFT Adapters (LoRA)**</br>
Low-rank adapters are injected into all key linear transformer blocks. Only adapter parameters are trainable, maintaining a frozen base model.

**QLoRA Strategy**</br>
Combines 8-bit quantization + frozen backbone + full-rank LoRA adapters—backpropagating exclusively through adapter weights. This replicates the QLoRA paradigm, achieving near full-precision fine-tuning performance with significantly reduced resource requirements 


**Training Engine (SFTTrainer from TRL)**</br>
Utilizes TRL’s SFTTrainer to conduct supervised fine-tuning on invoice data, optimizing only LoRA adapters under 8-bit quantization.



Training could be launched on single GPU or distributed GPU. </br>
For Single GPU:</br>
  - use llm_finetuning/smolvlm-trl-invoice.ipynb script. It is using HuggingFace TRL</br>
  - With Batch size of 4 and gradient_accumulation_steps 4, it takes around 21GB of RAM. </br>
 
For distributed training on multiple GPU:</br>
  - Use below  command to launch training job: </br>
    accelerate launch --config_file hf_accelerate_config.yaml run_vlm_sft_distributed.py --config smolvlm-qlora.yaml
    </br>
    Modified from - https://github.com/philschmid/deep-learning-pytorch-huggingface/blob/main/training/fine-tune-llms-in-2025.ipynb 