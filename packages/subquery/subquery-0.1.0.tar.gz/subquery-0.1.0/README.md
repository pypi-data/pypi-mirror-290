# Subquery Generator

This package provides functionality to generate subqueries and follow-up questions for a given input question.

## Installation

You can install the package with either the transformers or ollama backend:

```
pip install subquery[transformers]
```

or
bash
```
pip install subquery[ollama]
```

## Usage
For Transformers
```python
from subquery import TransformersSubqueryGenerator

# Using the Transformers backend
generator = TransformersSubqueryGenerator()
result = generator.generate("What is the capital of France?")

print("Follow-up questions:", result.follow_up)
print("Subqueries:", result.subquery)
```

```python
from subquery import OllamaSubqueryGenerator
# Using the Ollama backend
generator = OllamaSubqueryGenerator()
result = generator.generate("What is the capital of France?")

print("Follow-up questions:", result.follow_up)
print("Subqueries:", result.subquery)
```
