class MusicEvent:
    def __init__(self, note_name, duration, articulation=None, bow_part="G", is_tied=False):
        self.note_name = note_name
        self.duration = duration  # ex: 0.25 pour une noire
        self.articulation = articulation
        self.bow_part = bow_part
        self.is_tied = is_tied

    def get_real_duration(self):
        # Application de vos règles de transformation
        if self.articulation == "spiccato":
            return self.duration * 0.5
        elif self.articulation == "staccato":
            return self.duration * 0.75
        elif self.articulation == "staccatissimo":
            return self.duration * 0.25
        return self.duration

def compare_bowing(e1, e2):
    logique = []
    d1, d2 = e1.get_real_duration(), e2.get_real_duration()
    
    # Logique de Vitesse
    if d2 < d1 and e2.bow_part == e1.bow_part:
        logique.append("Vitesse : La 2ème note est plus courte sur la même zone, ralentir l'archet ou économiser la 1ère.")
    elif d2 > d1:
        logique.append("Vitesse : Accélérer progressivement pour maintenir l'intensité sur la note longue.")

    # Logique de Pression et Point de contact
    if "g" in e1.note_name.lower():
        logique.append("Point de contact : Corde de SOL, s'éloigner du chevalet, poids naturel du bras profond.")
    if "e" in e1.note_name.lower():
        logique.append("Point de contact : Corde de MI, se rapprocher du chevalet, pression index précise.")

    # Logique de liaison
    if e1.is_tied:
        logique.append("Liaison : Maintenir une pression constante malgré le changement de poids naturel (talon vers pointe).")
        
    return logique
