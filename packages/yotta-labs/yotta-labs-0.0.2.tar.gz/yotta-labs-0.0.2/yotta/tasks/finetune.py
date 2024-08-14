import torch

from transformers import AutoModelForCausalLM
from datasets import load_dataset
from transformers import Trainer, TrainingArguments


class FineTune:
    def __init__(self) -> None:
        pass

    def launch(
        self,
        *,
        dataset: str,
        model: str,
        epoch: int = 1,
        batch_size: int = 8,
        learning_rate: float = 0.00001,
        output_dir: str = "",
    ):

        model = AutoModelForCausalLM.from_pretrained(
            model, torch_dtype=torch.bfloat16, device_map="auto"
        )

        train_dataset = load_dataset(dataset, split="train")

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epoch,
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset["input"],
        )

        trainer.train()

        trainer.save_model(output_dir)
        return
