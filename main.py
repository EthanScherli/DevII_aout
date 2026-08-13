from monde import Lieu, Objet, MemoireMonde
from moteur import Joueur

def initialiser_jeu():
    memoire = MemoireMonde()
    
    # Création des lieux
    bibliotheque = Lieu("Bibliothèque", "Une vieille bibliothèque poussiéreuse. Une horloge arrêtée indique minuit.")
    bureau = Lieu("Bureau Secret", "Un petit bureau sombre. Vous vous sentez observé.")
    
    # Évolution du monde (Mécanique demandée par le client)
    bibliotheque.descriptions_alternatives["pris_Clé étrange"] = "La bibliothèque semble plus sombre depuis que vous avez pris la clé sur le bureau."
    
    # Création des objets
    cle = Objet("Clé étrange", "Une clé rouillée avec un symbole de corbeau.")
    bureau.ajouter_objet(cle)
    
    # Connexions
    bibliotheque.ajouter_sortie("nord", bureau)
    bureau.ajouter_sortie("sud", bibliotheque)
    
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