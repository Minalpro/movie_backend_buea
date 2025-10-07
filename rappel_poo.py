###### Classes, Object et attributs ######
# %%
class Chien:
    def __init__(self, nom, race, age):
        self.nom = nom
        self.race = race
        self.age = age
# %%

mon_chien = Chien("Rex", "Berger Allemand", 5)

# %%
print(mon_chien.nom)  # Affiche "Rex"
# %%
print(mon_chien.age) # Affiche 5
# %%
