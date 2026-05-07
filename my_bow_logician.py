import re

class SevcikBowLogician:
    def __init__(self):
        self.pos = 0.0  # 0=Talon, 1=Pointe
        self.last_note = None
        
    def analyze_note(self, lily_string):
        n = self._parse_note(lily_string)
        logique = []
        
        # --- 1. LOGIQUE DE PLACEMENT (Où commence/finit l'archet) ---
        start_label = self._pos_to_text(n['forced_start'] if n['forced_start'] is not None else self.pos)
        end_val = (n['forced_start'] if n['forced_start'] is not None else self.pos) + (n['frac'] * n['dir'])
        end_label = self._pos_to_text(end_val)
        
        logique.append(f"Coup d'archet : part du {start_label} vers le {end_label}.")

        # --- 2. LOGIQUE DE CORDES & POINT DE CONTACT (Distance Chevalet) ---
        contact = "Milieu (neutre)"
        if n['corde'] == 'IV': # Sol
            contact = "Plus loin du chevalet (corde épaisse, besoin de liberté)"
        elif n['corde'] == 'I': # Mi
            contact = "Plus près du chevalet (corde fine, besoin de brillance)"
        
        if n['nuance'] in ['f', 'ff']:
            contact = "Rapprocher du chevalet pour la résistance"
        elif n['nuance'] in ['p', 'pp']:
            contact = "Éloigner vers la touche (son flûté)"
        
        logique.append(f"Point de contact : {contact}.")

        # --- 3. LOGIQUE COMPARATIVE (Rythme et Intensité) ---
        if self.last_note:
            # Même longueur physique d'archet mais durée différente
            if n['frac'] == self.last_note['frac'] and n['dur_val'] > self.last_note['dur_val']:
                logique.append("Note plus longue pour même archet : ralentir et alléger la pression.")
            elif n['frac'] == self.last_note['frac'] and n['dur_val'] < self.last_note['dur_val']:
                logique.append("Note plus courte pour même archet : accélérer et appuyer davantage.")
            
            # Changement de nuance
            if n['nuance_level'] > self.last_note['nuance_level']:
                logique.append("Plus appuyé et plus rapide pour augmenter l'intensité.")
            elif n['nuance_level'] < self.last_note['nuance_level']:
                logique.append("Plus léger, relâcher la pression du bras.")

        # --- 4. ARTICULATION & VITESSE ---
        if n['articulation'] == 'staccato':
            logique.append("Vitesse : vive sur 3/4 de la note, puis arrêt net (pression maintenue).")
        elif n['articulation'] == 'spiccato':
            logique.append("Vitesse : lancée au milieu, rebondir à la moitié de la durée.")
        elif n['accent']:
            logique.append("Vitesse : Rapide-Lent (attaque subite puis économie).")
        else:
            logique.append("Vitesse : égale et constante sur toute la durée.")

        # --- 5. TENSION DU CRIN ---
        tension = "Souple et relâchée pour une belle sonorité ronde"
        if n['articulation'] in ['staccato', 'spiccato'] or n['nuance'] == 'ff':
            tension = "Plus tendue pour la précision du rebond et la morsure"
        logique.append(f"Tension du crin : {tension}.")

        self.pos = max(0, min(1, end_val))
        self.last_note = n
        return logique

    def _pos_to_text(self, val):
        if val <= 0.1: return "Talon"
        if val <= 0.4: return "Bas (entre talon et milieu)"
        if val <= 0.6: return "Milieu"
        if val <= 0.9: return "Haut (vers la pointe)"
        return "Pointe"

    def _parse_note(self, s):
        # Détection basique des éléments LilyPond
        return {
            'dir': -1 if "\\upbow" in s else 1,
            'frac': 0.5 if "1/2" in s else 0.33 if "1/3" in s else 0.25 if "1/4" in s else 1.0,
            'forced_start': 0.0 if '"Fr."' in s else 1.0 if '"Sp."' in s else 0.5 if '"M."' in s else None,
            'nuance': 'f' if '\\f' in s else 'p' if '\\p' in s else 'mf',
            'nuance_level': 3 if '\\f' in s else 1 if '\\p' in s else 2,
            'articulation': 'staccato' if '-.' in s else 'spiccato' if 'spicc' in s else 'normale',
            'accent': '->' in s or '-^' in s,
            'corde': 'IV' if 'IV' in s else 'I' if 'I' in s else 'II',
            'dur_val': 1.0 / int(re.search(r'\d+', s).group()) if re.search(r'\d+', s) else 0.25
        }

# --- TEST ---
script = SevcikBowLogician()
partition = [
    'g4\\downbow^"Fr."^"1/2"\\f IV', # Sol, Forte, Moitié, Talon
    'a4\\upbow^"1/2"\\p I',          # Mi, Piano, Même longueur mais plus léger
    'b8-.\\downbow^"1/4"'            # Staccato court
]

for note in partition:
    print(f"\n--- ANALYSE DE LA NOTE : {note} ---")
    for line in script.analyze_note(note):
        print(f"  > {line}")
