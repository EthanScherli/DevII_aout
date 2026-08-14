from monde import Lieu, Objet, MemoireMonde
from moteur import Joueur

def initialiser_jeu():
    memoire = MemoireMonde()
    
    # Création des lieux
    bibliotheque = Lieu("Bibliothèque", "Une vieille bibliothèque poussiéreuse. Une horloge arrêtée indique minuit.")
    bureau = Lieu("Bureau Secret", "Un petit bureau sombre. Vous vous sentez observé.")
    couloir = Lieu("Couloir Sombre", "Un passage étroit et lugubre. La lourde porte au sud semble verrouillée.")
    crypte = Lieu("Crypte", "Le cœur du mystère. L'air y est glacial.")
    
    # Évolution du monde (Mécanique demandée par le client)
    bibliotheque.descriptions_alternatives["pris_Clé étrange"] = "La bibliothèque semble plus sombre depuis que vous avez pris la clé sur le bureau."
    
    # Création des objets
    cle = Objet("Clé étrange", "Une lourde clé en fer forgé avec un crâne gravé.")
    bureau.ajouter_objet(cle)

    parchemin = Objet("Parchemin", "Note : 'La clé du savoir ouvre la porte des morts.'")
    bibliotheque.ajouter_objet(parchemin)

    relique = Objet("Relique", "L'Artéfact de la mort. Il palpite d'une énergie sombre.")
    crypte.ajouter_objet(relique)
    
    # Connexions
    bibliotheque.ajouter_sortie("nord", bureau)

    bureau.ajouter_sortie("sud", couloir)
    bureau.ajouter_sortie("sud", bibliotheque)
    
    couloir.ajouter_sortie("nord", bibliotheque)
    couloir.ajouter_sortie("sud", crypte)

    crypte.ajouter_sortie("nord", couloir)
    
    return Joueur(bibliotheque, memoire)

def demarrer():
    print("="*50)
    print(" BIENVENUE DANS L'AVENTURE DE LA MORT")
    print("Commandes: aller [nord/sud...], prendre [objet], examiner [lieu/objet], quitter")
    print("="*50)
    
    joueur = initialiser_jeu()
    print(joueur.executer_commande("examiner")) # Affiche la salle de départ
    
    while True:
        print("\n" + "-"*50)
        commande = input("> ")
        if commande.lower() in ["quitter", "exit", "quit"]:
            print("Merci d'avoir joué !")
            break
            
        reponse = joueur.executer_commande(commande)
        print("\n" + reponse)

if __name__ == "__main__":
    demarrer()