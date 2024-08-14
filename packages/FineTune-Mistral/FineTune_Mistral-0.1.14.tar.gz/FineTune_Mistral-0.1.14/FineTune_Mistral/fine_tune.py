import gc
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    MistralConfig  # Import the specific configuration class
)
from peft import LoraConfig, PeftModel
from random import randrange
from trl import SFTTrainer  # Correct import for the SFTTrainer

class FineTune_Mistral:
    def __init__(self, dataset_path, cache_dir, token):
        """
        Initialize the FineTune_Mistral class.

        Args:
            dataset_path (str): Path to the dataset.
            cache_dir (str): Directory to cache the models and tokenizers.
            token (str): Hugging Face API token for accessing gated repositories.

        How to obtain the Hugging Face API token:
        1. Go to https://huggingface.co/settings/tokens
        2. Log in or sign up if you don't have an account.
        3. Create a new token with the required permissions (read access is sufficient).
        4. Copy the token and provide it when initializing this class.
        """
        self.dataset_path = dataset_path
        self.cache_dir = cache_dir
        self.token = token

        # Embedded configuration
        config_dict = {
            "architectures": ["MistralForCausalLM"],
            "bos_token_id": 1,
            "eos_token_id": 2,
            "hidden_act": "silu",
            "hidden_size": 4096,
            "initializer_range": 0.02,
            "intermediate_size": 14336,
            "max_position_embeddings": 32768,
            "model_type": "mistral",
            "num_attention_heads": 32,
            "num_hidden_layers": 32,
            "num_key_value_heads": 8,
            "rms_norm_eps": 1e-05,
            "rope_theta": 10000.0,
            "sliding_window": 4096,
            "tie_word_embeddings": False,
            "torch_dtype": "bfloat16",
            "transformers_version": "4.34.0.dev0",
            "use_cache": True,
            "vocab_size": 32000
        }
        self.config = MistralConfig.from_dict(config_dict)  # Use the correct configuration class

        self.tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-v0.1", 
            cache_dir=self.cache_dir, 
            trust_remote_code=True,
            use_auth_token=self.token  # Use the correct parameter
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Set padding token to eos token
        self.tokenizer.padding_side = 'right'  # Ensure padding is on the right
        self.trained_model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-v0.1", 
            config=self.config,
            cache_dir=self.cache_dir,
            use_auth_token=self.token  # Use the correct parameter
        ).to("cuda")
        self.dataset = load_dataset('json', data_files=self.dataset_path, split='train')

    def train_model(self, output_dir, num_train_epochs=3, per_device_train_batch_size=2, per_device_eval_batch_size=1, max_seq_length=None):
        lora_config = LoraConfig(
            lora_alpha=16,
            lora_dropout=0.1,
            r=64,
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
                "lm_head",
            ],
            bias="none",
            task_type="CAUSAL_LM",
        )

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            logging_dir=f"{output_dir}/logs",
            logging_steps=100,
            save_steps=1000,
            warmup_ratio=0.03,
            report_to="tensorboard"
        )

        trainer = SFTTrainer(
            model=self.trained_model,
            train_dataset=self.dataset,
            peft_config=lora_config,
            dataset_text_field="text",  # Assuming 'text' is the field name containing the text data
            max_seq_length=max_seq_length,  # Pass None or specify a maximum sequence length
            tokenizer=self.tokenizer,
            args=training_args
        )

        trainer.train()
        trainer.model.save_pretrained(output_dir)
        print("The new model is available in " + output_dir)
        self.trained_model = trainer.model

    def generate_response(self, question, max_new_tokens=500, temperature=0.1):
        prompt = f"""You will be provided with a question. You must provide only a single answer. You must not provide additional questions and answers.
        Question:
        {question}
        """
        model_input = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            generated_code = self.trained_model.generate(**model_input, max_new_tokens=max_new_tokens, pad_token_id=0, temperature=temperature)
            generated_code = self.tokenizer.decode(generated_code[0], skip_special_tokens=True)
            response = generated_code.split("You will be provided with a question")[1]
            if len(response) < 10:
                return generated_code
        return response

    def clean_up(self):
        del self.tokenizer
        del self.trained_model
        gc.collect()
        torch.cuda.empty_cache()

    def selective_merge(self, base_model_path, fine_tuned_model_path, output_dir):
        base_model = AutoModelForCausalLM.from_pretrained(base_model_path, cache_dir=self.cache_dir, use_auth_token=self.token).to("cuda")
        fine_tuned_model = AutoModelForCausalLM.from_pretrained(fine_tuned_model_path, cache_dir=self.cache_dir, use_auth_token=self.token).to("cuda")

        # Extract state dicts
        base_state_dict = base_model.state_dict()
        ft_state_dict = fine_tuned_model.state_dict()

        # Filter out keys: only update base model with keys that exist in its state dict and have the same size
        for key in ft_state_dict:
            if key in base_state_dict and ft_state_dict[key].size() == base_state_dict[key].size():
                base_state_dict[key] = ft_state_dict[key]

        # Load the filtered state dict back into the base model
        base_model.load_state_dict(base_state_dict, strict=False)

        # Save the merged model
        base_model.save_pretrained(output_dir)

        return base_model
