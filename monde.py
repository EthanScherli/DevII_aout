class ActionInvalideError(Exception):
    """Exception levée quand le joueur tente une action impossible."""
    pass

class Objet:
    def __init__(self, nom, description):
        self._nom = nom
        self.description = description

    @property
    def nom(self):
        return self._nom

class PNJ:
    def __init__(self, nom, dialogue_base, dialogue_altere, condition_alteration):
        self._nom = nom
        self.dialogue_base = dialogue_base
        self.dialogue_altere = dialogue_altere
        self.condition_alteration = condition_alteration

    @property
    def nom(self):
        return self._nom

    def parler(self, memoire):
        # Le PNJ change de discours si la condition (ex: tuer le chien) est remplie
        if memoire.a_fait(self.condition_alteration):
            return self.dialogue_altere
        return self.dialogue_base

class Lieu:
    def __init__(self, nom, description_base):
        self.nom = nom
        self.description_base = description_base
        self.sorties = {}  # Dictionnaire des directions (ex: {'nord': lieu_suivant})
        self.objets = []
        self.pnjs = []
        # Demandé par le client : des descriptions qui changent selon les actions
        self.descriptions_alternatives = {} 

    def ajouter_sortie(self, direction, lieu):
        self.sorties[direction] = lieu

    def ajouter_objet(self, objet):
        self.objets.append(objet)

    def ajouter_pnj(self, pnj):
        self.pnjs.append(pnj)

    def retirer_objet(self, nom_objet):
        for obj in self.objets:
            if obj.nom.lower() == nom_objet.lower():
                self.objets.remove(obj)
                return obj
        return None

    def obtenir_description(self, memoire_jeu):
        """Retourne la description adaptée selon ce que le joueur a déjà fait."""
        for condition, nouvelle_desc in self.descriptions_alternatives.items():
            if memoire_jeu.a_fait(condition):
                return nouvelle_desc
        return self.description_base

class MemoireMonde:
    """Gère la mémoire des actions du joueur pour faire évoluer l'univers."""
    def __init__(self):
        self._actions_realisees = set()

    def retenir_action(self, action):
        self._actions_realisees.add(action)

    def a_fait(self, action):
        return action in self._actions_realisees