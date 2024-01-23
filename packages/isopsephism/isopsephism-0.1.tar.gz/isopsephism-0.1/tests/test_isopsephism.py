import pytest
from isopsephism.isopsephism import isopsephy

def test_from_greek_to_num():
    assert isopsephy.convert_word_to_num("ΚΟΥΡΑΙ") == 601

