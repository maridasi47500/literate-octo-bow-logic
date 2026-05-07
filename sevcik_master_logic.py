import re

class SevcikMasterLogic:
    def __init__(self):
        self.pos_actuelle = 0.0  # 0=Talon, 1=Pointe
        self.derniere_note = None

    def analyser(self, lily_string):
        # --- Extraction des données (Calculs cachés) ---
        n = self._extraire_physique(lily_string)
        instructions = []

        # 1. LOGIQUE DE PLACEMENT (Départ et Arrivée)
        depart = self._nommer_zone(n['start_force'] if n['start_force'] is not None else self.pos_actuelle)
        distance_parcourue = n['longueur_archet'] * n['direction']
        arrivee_val = (n['start_force'] if n['start_force'] is not None else self.pos_actuelle) + distance_parcourue
        arrivee = self._nommer_zone(arrivee_val)

        instructions.append(f"Archet : Poser au {depart}, finir au {arrivee}.")

        # 2. LOGIQUE DU POINT DE CONTACT (Distance au chevalet)
        # Calcul basé sur la corde et la nuance
        dist_chevalet = "Milieu de l'espace de jeu"
        if n['corde'] == 'IV': dist_chevalet = "S'éloigner du chevalet (Corde Sol)"
        if n['corde'] == 'I':  dist_chevalet = "Se rapprocher du chevalet (Corde Mi)"
        
        if n['nuance'] == 'f': dist_chevalet = "Chercher la résistance près du chevalet"
        if n['nuance'] == 'p': dist_chevalet = "Glisser vers la touche (alléger le timbre)"
        
        instructions.append(f"Point de contact : {dist_chevalet}.")

        # 3. LOGIQUE DE COMPARAISON (L'intelligence du mouvement)
        if self.derniere_note:
            # Même longueur d'archet, mais durée différente
            if n['longueur_archet'] == self.derniere_note['longueur_archet']:
                if n['duree_temporelle'] > self.derniere_note['duree_temporelle']:
                    instructions.append("Même archet mais note plus longue : ralentir le geste et relâcher la pression pour ne pas écraser.")
                elif n['duree_temporelle'] < self.derniere_note['duree_temporelle']:
                    instructions.append("Même archet mais note plus courte : accélérer le geste et mordre davantage la corde.")
            
            # Nuance changeante
            if n['nuance_poids'] > self.derniere_note['nuance_poids']:
                instructions.append("Augmenter le poids du bras de façon progressive.")
            elif n['nuance_poids'] < self.derniere_note['nuance_poids']:
                instructions.append("Alléger l'index, laisser l'archet respirer.")

        # 4. VITESSE ET TENSION
        if n['articulation'] == 'staccato':
            instructions.append("Vitesse : Vive au départ, arrêt net à 3/4 de la note, garder le crin collé.")
            instructions.append("Tension : Crin tendu pour un rebond précis.")
        elif n['articulation'] == 'spiccato':
            instructions.append("Vitesse : Lancée, laisser l'archet rebondir naturellement au milieu.")
        else:
            instructions.append("Vitesse : Geste fluide et constant.")

        # Mise à jour pour la note suivante
        self.pos_actuelle = max(0, min(1, arrivee_val))
        self.derniere_note = n
        return instructions

    def _nommer_zone(self, val):
        if val <= 0.1: return "Talon"
        if val <= 0.35: return "Bas"
        if val <= 0.65: return "Milieu"
        if val <= 0.9: return "Haut"
        return "Pointe"

    def _extraire_physique(self, s):
        # Ici Python calcule mais ne montre rien
        return {
            'direction': -1 if "\\upbow" in s else 1,
            'longueur_archet': 0.5 if "1/2" in s else 0.33 if "1/3" in s else 0.25 if "1/4" in s else 0.1,
            'start_force': 0.0 if '"Fr."' in s else 1.0 if '"Sp."' in s else 0.5 if '"M."' in s else None,
            'nuance': 'f' if '\\f' in s else 'p' if '\\p' in s else 'mf',
            'nuance_poids': 3 if '\\f' in s else 1 if '\\p' in s else 2,
            'articulation': 'staccato' if '-.' in s else 'spiccato' if 'spicc' in s else 'normale',
            'corde': 'IV' if 'IV' in s else 'I' if 'I' in s else 'II',
            'duree_temporelle': 1.0 / int(re.search(r'\d+', s).group()) if re.search(r'\d+', s) else 0.25
        }

# --- APPLICATION PRATIQUE ---
logicien = SevcikMasterLogic()
partition = [
    'g4\\downbow^"Fr."^"1/2"\\f IV', 
    'a4\\upbow^"1/2"\\p I', 
    'b2\\downbow^"WB"\\mf'
]

for note in partition:
    print(f"\nANALYSE TECHNIQUE : {note}")
    for conseil in logicien.analyser(note):
        print(f"  • {conseil}")
