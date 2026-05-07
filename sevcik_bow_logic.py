import re

class SevcikFullLogic:
    def __init__(self):
        # État de l'archet
        self.pos = 0.0          # 0=Talon, 1=Pointe
        self.direction = 1       # 1=Tiré, -1=Poussé
        self.on_string = True    # Contact avec la corde
        
        # Mapping des fractions Ševčík
        self.fractions = {
            '"1/2"': 0.5, '"1/3"': 0.33, '"2/3"': 0.66,
            '"1/4"': 0.25, '"3/4"': 0.75, '"G.B."': 1.0, '"WB"': 1.0
        }

    def analyze_note(self, lily_string):
        status = {"alerts": []}
        
        # 1. Gestion de la Direction
        if "\\downbow" in lily_string: self.direction = 1
        if "\\upbow" in lily_string: self.direction = -1
        
        # 2. Gestion de la Levée d'archet (Symboles: , ou \breath)
        if "," in lily_string or "\\breath" in lily_string:
            self.on_string = False
            status["action"] = "Lever l'archet"
        else:
            self.on_string = True

        # 3. Positionnement Forcé (Talon/Milieu/Pointe)
        if '"Fr."' in lily_string: self.pos = 0.0
        if '"M."' in lily_string: self.pos = 0.5
        if '"Sp."' in lily_string: self.pos = 1.0

        # 4. Calcul de la consommation d'archet
        consommation = 0.0
        for frac_str, value in self.fractions.items():
            if frac_str in lily_string:
                consommation = value
                break
        
        # Si aucune fraction, on estime selon la durée (ex: 4 = 1/4 d'archet par défaut)
        if consommation == 0.0:
            dur_match = re.search(r'\d+', lily_string)
            consommation = 1/int(dur_match.group()) if dur_match else 0.25

        # 5. Application des Articulations (Staccato/Spiccato)
        pression = 5  # Échelle 1-10
        if "-." in lily_string: # Staccato
            pression += 2
            status["vitesse"] = "Sèche"
        if "\\pointAndClick" in lily_string or "spicc" in lily_string: # Spiccato
            status["mode"] = "Sautillé"
            pression = 2

        # 6. Calcul du mouvement physique
        mouvement = consommation * self.direction
        nouvelle_pos = self.pos + mouvement
        
        # Vérification des limites physiques de l'archet
        if nouvelle_pos > 1.0 or nouvelle_pos < 0.0:
            status["alerts"].append("DÉBORDEMENT : Manque de longueur d'archet !")
        
        self.pos = max(0.0, min(1.0, nouvelle_pos))
        
        # 7. Données de sortie
        status["pos_finale"] = round(self.pos, 2)
        status["pression_estimee"] = pression
        return status

# --- EXEMPLE D'UTILISATION ---
engine = SevcikFullLogic()
# Simulation d'une séquence Ševčík : Tiré talon moitié, Poussé quart, Lever
sequence = [
    'c4\\downbow^"Fr."^"1/2"', 
    'd8\\upbow^"1/4"', 
    'e4\\downbow-."1/4"', 
    'g4\\upbow^","'
]

print(f"{'Note':<20} | {'Pos. Finale':<12} | {'Alertes'}")
print("-" * 50)
for n in sequence:
    res = engine.analyze_note(n)
    alert = res["alerts"][0] if res["alerts"] else "OK"
    print(f"{n:<20} | {res['pos_finale']:<12} | {alert}")
