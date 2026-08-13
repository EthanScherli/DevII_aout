import datetime
from monde import ActionInvalideError

def log_action(func):
    def wrapper(joueur, *args, **kwargs):
        resultat = func(joueur, *args, **kwargs)
        with open("logs_partie.txt", "a", encoding="utf-8") as f:
            date_heure = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commande = " ".join(args) if args else "Action interne"
            f.write(f"[{date_heure}] Commande: '{commande}' | Résultat: {resultat}\n")
        return resultat
    return wrapper

class Joueur:
    def __init__(self, lieu_depart, memoire):
        self.lieu_actuel = lieu_depart
        self.inventaire = []
        self.memoire = memoire

    def possede_objet(self, nom_objet):
        objets_trouves = list(filter(lambda obj: obj.nom.lower() == nom_objet.lower(), self.inventaire))
        return objets_trouves[0] if objets_trouves else None

    @log_action
    def executer_commande(self, commande_brute):
        mots = commande_brute.lower().strip().split()
        if not mots:
            return "Veuillez entrer une commande."

        verbe = mots[0]
        cible = " ".join(mots[1:]) if len(mots) > 1 else ""

        try:
            if verbe in ["aller", "deplacer"]:
                return self._aller(cible)
            elif verbe in ["prendre", "ramasser"]:
                return self._prendre(cible)
            elif verbe in ["examiner", "regarder"]:
                return self._examiner(cible)
            else:
                return "Je ne comprends pas cette commande. Essayez 'aller [direction]', 'prendre [objet]', 'examiner [objet/lieu]'."
        except ActionInvalideError as e:
            return str(e)

    def _aller(self, direction):
        if direction in self.lieu_actuel.sorties:
            self.lieu_actuel = self.lieu_actuel.sorties[direction]
            return f"Vous allez vers le {direction}.\n\n" + self._examiner("")
        raise ActionInvalideError(f"Vous ne pouvez pas aller par là : {direction}.")

    def _prendre(self, cible):
        objet = self.lieu_actuel.retirer_objet(cible)
        if objet:
            self.inventaire.append(objet)
            self.memoire.retenir_action(f"pris_{objet.nom}")
            return f"Vous avez pris : {objet.nom}."
        raise ActionInvalideError(f"Il n'y a pas de '{cible}' ici.")

    def _examiner(self, cible):
        if cible == "" or cible == "lieu" or cible == "piece":
            desc = self.lieu_actuel.obtenir_description(self.memoire)
            objets_ici = ", ".join([obj.nom for obj in self.lieu_actuel.objets])
            if objets_ici:
                desc += f"\nVous voyez ici : {objets_ici}."
            return desc
        
        obj_inv = self.possede_objet(cible)
        if obj_inv:
            return f"Dans votre inventaire : {obj_inv.description}"
        
        raise ActionInvalideError(f"Vous ne voyez rien de tel ({cible}) à examiner.")