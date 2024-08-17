# Subquery

`Subquery` generates subqueries and follow-up questions for a given input question.
Using the EXTREMELY SMOLL LLM [subquery-SmolLM](https://huggingface.co/andthattoo/subquery-SmolLM)
It's a finetuned model based on [nisten/Biggie-SmoLlm-0.15B-Base](https://huggingface.co/nisten/Biggie-SmoLlm-0.15B-Base)

tiny as 150M (or 180M) parameters and thanks to wonderful work by Nisten and Huggingface's [SmolLM-135M](https://huggingface.co/HuggingFaceTB/SmolLM-135M)

It can run both with `transformers` and `ollama` backends.
Ollama based GGUF model runs at 160 tps for 1 CPU. 

yes.

It can do two things:

1. Generate subqueries for a given question.
![q1](misc/ss1.jpg)
2. Generate follow-up questions for a vague question.
![q2](misc/ss2.jpg)

This package wraps the model and provides a simple interface to generate subqueries and follow-up questions.

## Installation

You can install the package with

```
pip install subquery
```

## Usage
For Transformers
```python
from subquery import TransformersSubqueryGenerator

# Using the Transformers backend
generator = TransformersSubqueryGenerator()
result = generator.generate("What is this?")

print("Follow-up questions:", result.follow_up)
print("Subqueries:", result.subquery)
```
For Ollama
```python
from subquery import OllamaSubqueryGenerator
# Using the Ollama backend
generator = OllamaSubqueryGenerator()
result = generator.generate("Are the Indiana Harbor and Ship Canal and the Folsom South Canal in the same state?")

print("Follow-up questions:", result.follow_up)
print("Subqueries:", result.subquery)
```
