# Creation d'un objet calculatrice
# %%
class Calculator:
    def __init__(self):
        pass
# %%
    def add(self, a, b):
        return a + b
# %%
    def subtract(self, a, b):
        return a - b
# %%
    def multiply(self, a, b):
        return a * b
# %%
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
# %%
# Exemple d'utilisation
calc = Calculator()
print(calc.add(5, 3))        
print(calc.subtract(10, 4))
print(calc.multiply(2, 6))
# %%
