class BowLogic:
    def __init__(self):
        pass

    # -------------------------
    # 1. Tables de base
    # -------------------------

    natural_pressure = {
        "talon": 3,     # lourd
        "milieu": 2,    # neutre
        "pointe": 1     # léger
    }

    bow_fraction_factor = {
        "1/1": 1.0,
        "1/2": 0.5,
        "1/3": 0.33,
        "1/4": 0.25
    }

    duration_factor = {
        "longue": 0.5,   # vitesse lente
        "normale": 1.0,
        "courte": 2.0    # vitesse rapide
    }

    nuance_factor = {
        "p": 0.7,
        "f": 1.3
    }

    string_factor = {
        "sol": 1.3,
        "mi": 0.8
    }

    articulation_duration = {
        "legato": 1.0,
        "staccato": 0.75,
        "spiccato": 0.5
    }

    # -------------------------
    # 2. Calcul principal
    # -------------------------

    def compute(self, position, fraction, duration, nuance, articulation, string):

        # vitesse = durée × fraction
        speed = self.duration_factor[duration] / self.bow_fraction_factor[fraction]

        # pression = pression naturelle × nuance × corde
        pressure = (
            self.natural_pressure[position] *
            self.nuance_factor[nuance] *
            self.string_factor[string]
        )

        # articulation influence
        effective_duration = self.articulation_duration[articulation]

        # -------------------------
        # 3. Détection d’erreurs logiques
        # -------------------------
        errors = []

        # Erreur 1 : spiccato hors du milieu
        if articulation == "spiccato" and position != "milieu":
            errors.append("Spiccato impossible hors du milieu de l’archet.")

        # Erreur 2 : écrasement
        if speed > 1.5 and pressure > 3:
            errors.append("Écrasement : vitesse trop rapide + pression trop forte.")

        # Erreur 3 : sifflement
        if speed < 0.7 and pressure < 1.5:
            errors.append("Sifflement : vitesse trop lente + pression trop faible.")

        # Erreur 4 : forte à la pointe
        if nuance == "f" and position == "pointe":
            errors.append("Forte à la pointe : nécessite pression artificielle.")

        # Erreur 5 : piano au talon
        if nuance == "p" and position == "talon":
            errors.append("Piano au talon : nécessite soutien de l’archet.")

        return {
            "vitesse": round(speed, 2),
            "pression": round(pressure, 2),
            "durée_effective": effective_duration,
            "erreurs": errors
        }
