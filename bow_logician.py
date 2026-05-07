import re

class SevcikBowLogician:
    def __init__(self):
        # État interne de l'archet
        self.current_pos = 0.0  # 0=Talon, 1=Pointe
        self.prev_note = None
        
        # Dictionnaire des durées LilyPond
        self.durations = {'1': 4.0, '2': 2.0, '4': 1.0, '8': 0.5, '16': 0.25, '32': 0.125}

    def _get_note_data(self, lily_note):
        """Extrait les propriétés physiques d'une note LilyPond."""
        data = {
            'duration': 1.0,
            'direction': 'inconnu',
            'fraction': None,
            'position_forcee': None,
            'articulation': 'ordinaire',
            'nuance': 'mf'
        }
        
        # Extraction durée
        dur_match = re.search(r'\d+', lily_note)
        if dur_match:
            data['duration'] = self.durations.get(dur_match.group(), 1.0)
            
        # Direction
        if "\\downbow" in lily_note: data['direction'] = "Tiré"
        if "\\upbow" in lily_note: data['direction'] = "Poussé"
        
        # Fractions Ševčík
        for f in ["1/2", "1/3", "2/3", "1/4", "3/4"]:
            if f'"{f}"' in lily_note: data['fraction'] = f
            
        # Position de départ
        if '"Fr."' in lily_note: data['position_forcee'] = 0.0
        if '"M."' in lily_note: data['position_forcee'] = 0.5
        if '"Sp."' in lily_note: data['position_forcee'] = 1.0
        
        # Articulations
        if "-." in lily_note: data['articulation'] = 'staccato'
        if "spicc" in lily_note or "\\point" in lily_note: data['articulation'] = 'spiccato'
        if "-^" in lily_note: data['articulation'] = 'martelé'
        
        # Nuances
        for n in ['pp', 'p', 'mp', 'mf', 'f', 'ff']:
            if f"\\{n}" in lily_note: data['nuance'] = n
            
        return data

    def analyze_sequence(self, notes_list):
        print(f"{'NOTE':<20} | {'LOGIQUE DE L''ARCHET'}")
        print("-" * 70)
        
        for i, raw_note in enumerate(notes_list):
            current = self._get_note_data(raw_note)
            logic_msg = []
            
            # 1. Gestion de la position et longueur
            if current['position_forcee'] is not None:
                pos_name = "Talon" if current['position_forcee'] == 0 else "Pointe" if current['position_forcee'] == 1 else "Milieu"
                logic_msg.append(f"Démarrer au {pos_name}")
                self.current_pos = current['position_forcee']

            # 2. Logique de Vitesse et Pression relative
            if self.prev_note:
                # Comparaison de durée
                if current['duration'] > self.prev_note['duration']:
                    logic_msg.append("Allonger l'archet")
                elif current['duration'] < self.prev_note['duration']:
                    logic_msg.append("Économiser l'archet (mouvement court)")
                
                # Logique Pression/Vitesse (Intensité)
                if current['nuance'] == self.prev_note['nuance'] and current['duration'] < self.prev_note['duration']:
                    logic_msg.append("Appuyer PLUS (compensation durée courte)")
                elif current['articulation'] == 'staccato':
                    logic_msg.append("Pression subite, arrêt net à 3/4")
                elif current['articulation'] == 'spiccato':
                    logic_msg.append("Lancer l'archet (rebond milieu), durée 1/2")

            # 3. Logique de la fraction Ševčík
            if current['fraction']:
                logic_msg.append(f"Utiliser strictement {current['fraction']} de la baguette")

            # 4. Déplacement de l'archet
            dist = float(eval(current['fraction'])) if current['fraction'] else (0.25 if current['duration'] <= 1 else 0.5)
            direction_sign = 1 if current['direction'] == "Tiré" else -1
            self.current_pos += (dist * direction_sign)
            
            # 5. Alerte de fin d'archet
            if self.current_pos > 1.0: logic_msg.append("ATTENTION: Trop près de la pointe !")
            if self.current_pos < 0.0: logic_msg.append("ATTENTION: Trop près du talon !")

            print(f"{raw_note:<20} | {', '.join(logic_msg)}")
            self.prev_note = current

# --- EXEMPLE DE TEST ---
logician = SevcikBowLogician()
partition_sevcik = [
    'c4\\downbow^"Fr."\\f',        # Note de départ forte au talon
    'd8\\upbow^"1/4"',              # Note courte, un quart d'archet
    'e2\\downbow^"1/2"\\p',         # Note longue mais piano
    'f4-.\\upbow',                  # Staccato
    'g8\\downbow\\spiccato'         # Spiccato
]

logician.analyze_sequence(partition_sevcik)
