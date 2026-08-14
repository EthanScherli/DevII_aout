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
            elif verbe in ["parler", "discuter"]:
                return self._parler(cible)
            elif verbe in ["attendre", "patienter"]:
                return self._attendre()
            elif verbe == "tuer":
                return self._tuer(cible)
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

            # Affichage des PNJs et du chien
            if self.lieu_actuel.pnjs:
                pnjs_ici = ", ".join([pnj.nom for pnj in self.lieu_actuel.pnjs])
                desc += f"\nQuelqu'un se trouve ici : {pnjs_ici}."
                if not self.memoire.a_fait("chien_mort") and any(p.nom == "Gardien" for p in self.lieu_actuel.pnjs):
                    desc += " Un petit chien repose paisiblement à ses côtés."
            
            # Affichage des objets
            objets_ici = ", ".join([obj.nom for obj in self.lieu_actuel.objets])
            if objets_ici:
                desc += f"\nVous voyez ici : {objets_ici}."
            return desc
        
        obj_inv = self.possede_objet(cible)
        if obj_inv:
            return f"Dans votre inventaire : {obj_inv.description}"
        
        raise ActionInvalideError(f"Vous ne voyez rien de tel ({cible}) à examiner.")

    def _parler(self, cible):
        if not cible:
            raise ActionInvalideError("À qui voulez-vous parler ? (ex: parler gardien)")
            
        for pnj in self.lieu_actuel.pnjs:
            if pnj.nom.lower() == cible.lower():
                return f"{pnj.nom} vous dévisage et dit : « {pnj.parler(self.memoire)} »"
        raise ActionInvalideError(f"Il n'y a personne nommé '{cible}' ici.")

    def _attendre(self):
        self.memoire.retenir_action("a_attendu")
        return "Vous attendez dans le silence... Soudain, une pulsion sombre et incontrôlable s'empare de vous. Vos mains se mettent à trembler. Une voix effroyable murmure dans votre tête : 'Le chien... tue le chien...'"

    def _tuer(self, cible):
        if cible == "chien":
            # On vérifie qu'on est bien dans la pièce avec le Gardien
            if any(pnj.nom == "Gardien" for pnj in self.lieu_actuel.pnjs):
                if self.memoire.a_fait("chien_mort"):
                    raise ActionInvalideError("Le chien est déjà mort, vous avez fait assez de dégâts.")
                
                # Le joueur ne peut tuer le chien que s'il a eu la pulsion (a_attendu)
                if self.memoire.a_fait("a_attendu"):
                    self.memoire.retenir_action("chien_mort")
                    return "Empli d'une rage soudaine et irrationnelle, vous abattez le pauvre chien sans pitié. Le Gardien hurle de désespoir et vous regarde avec des yeux remplis de haine."
                else:
                    raise ActionInvalideError("Tuer ce pauvre animal ? Quelle idée abominable, vous n'avez aucune raison de faire ça.")
            else:
                raise ActionInvalideError("Il n'y a pas de chien ici.")
        raise ActionInvalideError(f"Vous ne pouvez pas attaquer {cible}.")

    def _aller(self, direction):
        if direction in self.lieu_actuel.sorties:
            lieu_cible = self.lieu_actuel.sorties[direction]
            
            # --- NOUVELLE LOGIQUE D'INVENTAIRE ---
            if lieu_cible.nom == "Crypte" and not self.possede_objet("Clé étrange"):
                raise ActionInvalideError("La porte de la Crypte est verrouillée. Il vous manque la bonne clé.")
            # -------------------------------------
                
            self.lieu_actuel = lieu_cible
            return f"Vous allez vers le {direction}.\n\n" + self._examiner("")
        raise ActionInvalideError(f"Vous ne pouvez pas aller par là : {direction}.")