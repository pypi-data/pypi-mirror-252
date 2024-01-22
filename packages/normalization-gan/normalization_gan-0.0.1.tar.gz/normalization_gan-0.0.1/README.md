## Python library for text normalization for TTS input using gpt

# Installation

```bash
pip install normalization_gan
```
# Usage

```python
from normalization_gan import Normalization

# Create instance, provide openai_api_key as string to authenticate
normalization_obj = Normalization(OPENAI_API_KEY)

sample_text = "My phone number is 555-1234"

# Use normalize_text method 
normalized_text = normalization_obj.normalize_text(sample_text)

# Output string would look like : "My phone number is five five five one two three four."
```

