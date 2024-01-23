

class LetterToNumberConverter(object):

    def __init__(self, dict):
        self.dict = dict


    def convert_word_to_num(self, word):
        number = 0
        for x in word:
            number += self.dict.get(x)

        return number
        






    

greek_isopsephy_dict = {
    "Α": 1,
    "α": 1,
    "Β": 2,
    "β": 2,
    "Γ": 3,
    "γ": 3,
    "Δ": 4,
    "δ": 4,
    "Ε": 5,
    "ε": 5,
    "Ϝ": 6,
    "ϝ": 6,
    "Ϛ": 6,
    "ϛ": 6,
    "Y": 7,
    "Y": 7,
    "Η": 8,
    "η": 8,
    "Θ": 9,
    "θ": 9,
    "Ι": 10,
    "ι": 10,
    "Κ": 20,
    "κ": 20,
    "Λ": 30,
    "λ": 30,
    "Μ": 40,
    "μ": 40,
    "Ν": 50,
    "ν": 50,
    "Ξ": 60,
    "ξ": 60,
    "Ο": 70,
    "ο": 70,
    "Π": 80,
    "π": 80,
    "Ϙ": 90,
    "ϙ": 90,
    "Ρ": 100,
    "ρ": 100,
    "Σ": 200,
    "σ": 200,
    "Τ": 300,
    "τ": 300,
    "Υ": 400,
    "υ": 400,
    "Φ": 500,
    "φ": 500,
    "Χ": 600,
    "χ": 600,
    "Ψ": 700,
    "ψ": 700,
    "Ω": 800,
    "ω": 800,
    "Ϡ": 900,
    "ϡ": 900
}

isopsephy = LetterToNumberConverter(greek_isopsephy_dict)
