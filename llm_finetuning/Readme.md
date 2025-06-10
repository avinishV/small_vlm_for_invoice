Use below  script to launch training job: </br>
accelerate launch --config_file hf_accelerate_config.yaml run_vlm_sft_distributed.py --config smolvlm-qlora.yaml

</br>
Modified from - https://github.com/philschmid/deep-learning-pytorch-huggingface/blob/main/training/fine-tune-llms-in-2025.ipynb 