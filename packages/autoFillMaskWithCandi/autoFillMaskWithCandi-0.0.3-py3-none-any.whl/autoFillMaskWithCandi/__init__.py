"""
My NLP Package
This package provides functionalities for processing and comparing sentences
using models from Hugging Face's Transformers library.
"""

__version__ = '1.0.0'

# Import key functions/classes from your modules for easier access
from .autoFillMaskWithCandi import setTokenModel, mask_differing_words, show_mask_fill, mask_fill_replaced
