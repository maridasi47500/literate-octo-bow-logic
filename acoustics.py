import re

class SevcikLogicalAcoustics:
    def __init__(self):
        self.pos = 0.0  # 0.0 (Talon) à 1.0 (Pointe)
        self.prev = None
        self.tension_crin = "Moyenne (idéale pour l'articulation)"
        
        # Constantes physiques par corde
        self.cordes = {
            'I':  {'nom': 'Mi', 'dist_chevalet': 'Près (Timbre brillant)', 'pression_base': 3},
            'II': {'nom': 'La', 'dist_chevalet': 'Intermédiaire', 'pression_base': 4},
            'III':{'nom': 'Ré', 'dist_chevalet': 'Intermédiaire', 'pression_base': 5},
            'IV': {'nom': 'Sol', 'dist_chevalet': 'Loin (Éviter l\'écrasement)', 'pression_base': 6}
        }

    def analyze(self, lily_string):
        # 1. Parsing complet de la note
        n = self._parse_lily(lily_string)
        logique = []
        physique = {}

        # 2. LOGIQUE DE VITESSE ET RÉPARTITION
        # Calcul du segment précis
        start_pos = n['start_pos'] if n['start_pos'] is not None else self.pos
        length = n['frac_val']
        end_pos = start_pos + (length * n['dir_sign'])
        
        physique['segment'] = f"De {int(start_pos*100)}% à {int(end_pos*100)}% de la baguette"

        # Vitesse : Égale ou Variable ?
        if n['accent']:
            physique['vitesse'] = "Vitesse explosive (Rapide -> Lent)"
            physique['pression'] = "Forte attaque, puis relâchement immédiat"
        elif n['articulation'] == 'staccato':
            physique['vitesse'] = "Rapide et courte (Arrêt sec)"
            physique['pression'] = "Constante et mordante"
        else:
            physique['vitesse'] = "Vitesse égale et soutenue"
            physique['pression'] = "Équilibrée"

        # 3. POINT DE CONTACT (Distance au chevalet)
        corde_info = self.cordes.get(n['corde'], self.cordes['II'])
        dist = corde_info['dist_chevalet']
        if n['nuance'] in ['f', 'ff']:
            dist = "Plus près du chevalet (Résistance accrue)"
        elif n['nuance'] in ['p', 'pp']:
            dist = "Vers la touche (Flautando)"
        physique['point_contact'] = dist

        # 4. LOGIQUE COMPARATIVE (Conseils de jeu)
        if self.prev:
            # Comparaison de longueur
            if n['frac_val'] > self.prev['frac_val']:
                logique.append("Note plus allongée que la précédente")
            elif n['frac_val'] < self.prev['frac_val']:
                logique.append("Note plus courte, économiser l'archet")
            
            # Comparaison de pression
            if n['nuance_val'] > self.prev['nuance_val']:
                logique.append("Appuyer PLUS (pression croissante)")
            elif n['nuance_val'] < self.prev['nuance_val']:
                logique.append("Relâcher la pression (poids du bras allégé)")

        # 5. TENSION DU CRIN
        if n['articulation'] in ['spiccato', 'martelé']:
            self.tension_crin = "Plus tendue (pour favoriser le rebond et l'attaque)"
        else:
            self.tension_crin = "Souple (pour maximiser la surface de contact)"

        # Mise à jour de l'état
        self.pos = max(0, min(1, end_pos))
        self.prev = n
        
        return physique, logique

    def _parse_lily(self, s):
        # Extraction simplifiée pour l'exemple
        dir_sign = -1 if "\\upbow" in s else 1
        frac = 1.0
        if "1/2" in s: frac = 0.5
        if "1/4" in s: frac = 0.25
        if "1/3" in s: frac = 0.33
        
        return {
            'dir_sign': dir_sign,
            'frac_val': frac,
            'start_pos': 0.0 if '"Fr."' in s else 1.0 if '"Sp."' in s else None,
            'nuance': 'f' if '\\f' in s else 'p' if '\\p' in s else 'mf',
            'nuance_val': 3 if '\\f' in s else 1 if '\\p' in s else 2,
            'articulation': 'staccato' if '-.' in s else 'spiccato' if 'spicc' in s else 'normal',
            'accent': True if '->' in s or '-^' in s else False,
            'corde': 'IV' if 'IV' in s else 'I' if 'I' in s else 'II'
        }

# --- TEST ---
script = SevcikLogicalAcoustics()
exercice = [
    'g4\\downbow^"Fr."^"1/2"\\f IV',  # Corde Sol, Forte, Moitié, au talon
    'a8\\upbow^"1/4"\\p',              # Plus court, Piano
    'b4-.\\downbow->'                  # Staccato avec accent
]

for note in exercice:
    phys, log = script.analyze(note)
    print(f"\nANALYSE : {note}")
    print(f"  - Logique : {', '.join(log) if log else 'Initialisation'}")
    print(f"  - Physique : {phys['segment']} | {phys['vitesse']}")
    print(f"  - Point de contact : {phys['point_contact']}")
    print(f"  - Crin : {script.tension_crin}")
