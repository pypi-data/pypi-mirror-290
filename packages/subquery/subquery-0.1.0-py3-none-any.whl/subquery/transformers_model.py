import re
import torch
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
from .core import SubqueryGenerator, SubqueryResult
from typing import List
import importlib.util


def check_transformers():
    if importlib.util.find_spec("transformers") is None or importlib.util.find_spec("torch") is None:
        raise ImportError("Transformers and torch must be installed to use TransformersSubqueryGenerator. "
                          "Install subquery with the [transformers] extra.")

# The rest of the file remains the same


class TransformersSubqueryGenerator(SubqueryGenerator):
    def __init__(self):
        check_transformers()
        self.config = AutoConfig.from_pretrained("andthattoo/subquery-SmolLM")
        self.tokenizer = AutoTokenizer.from_pretrained("andthattoo/subquery-SmolLM")
        self.model = AutoModelForCausalLM.from_pretrained("andthattoo/subquery-SmolLM", torch_dtype=torch.bfloat16)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.model.config.eos_token_id
    @staticmethod
    def get_text_between_tags(text: str, tag: str) -> List[str]:
        pattern = f'<{tag}>(.*?)</{tag}>'
        return re.findall(pattern, text, re.DOTALL)

    def generate(self, question: str) -> SubqueryResult:
        input_data = f"Generate subqueries for a given question. <question>{question}</question>"
        inputs = self.tokenizer(input_data, return_tensors='pt')
        output = self.model.generate(**inputs, max_new_tokens=100)
        decoded_output = self.tokenizer.decode(output[0], skip_special_tokens=True)

        follow_ups = self.get_text_between_tags(decoded_output, "follow_up")
        subqueries = self.get_text_between_tags(decoded_output, "subquery")

        follow_ups = list(set([s.lower() for s in follow_ups]))
        subqueries = list(set([s.lower() for s in subqueries]))

        return SubqueryResult(follow_ups, subqueries)