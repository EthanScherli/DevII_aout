import tkinter as tk
from tkinter import scrolledtext
from main import initialiser_jeu  

class InterfaceJeu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("MiamCorp - Aventure Textuelle")
        self.fenetre.geometry("700x500")
        self.fenetre.configure(bg="black")
        
        # Initialisation du moteur de jeu
        self.joueur = initialiser_jeu()

        # 1. Zone d'affichage du texte (Historique et descriptions)
        self.zone_texte = scrolledtext.ScrolledText(
            fenetre, wrap=tk.WORD, bg="black", fg="lightgreen", 
            font=("Courier", 11), state=tk.NORMAL
        )
        self.zone_texte.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Message de bienvenue et première description
        self.ajouter_texte("="*50 + "\n BIENVENUE DANS L'AVENTURE DE LA MORT \n" + "="*50 + "\n")
        self.ajouter_texte(self.joueur.executer_commande("examiner") + "\n")

        # Conteneur pour la zone de saisie et le bouton
        cadre_bas = tk.Frame(fenetre, bg="black")
        cadre_bas.pack(fill=tk.X, padx=10, pady=(0, 10))

        # 2. Barre de saisie pour taper les commandes
        self.entree_commande = tk.Entry(
            cadre_bas, font=("Courier", 12), bg="gray15", fg="white", insertbackground="white"
        )
        self.entree_commande.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entree_commande.bind("<Return>", self.traiter_commande)  # Permet de valider avec la touche Entrée
        self.entree_commande.focus()

        # 3. Bouton "Valider"
        self.bouton_valider = tk.Button(
            cadre_bas, text="Action !", bg="green", fg="white", 
            font=("Courier", 10, "bold"), command=self.traiter_commande
        )
        self.bouton_valider.pack(side=tk.RIGHT)

    def ajouter_texte(self, texte):
        """Permet d'ajouter du texte dans la zone de lecture en la déverrouillant temporairement."""
        self.zone_texte.config(state=tk.NORMAL)
        self.zone_texte.insert(tk.END, texte + "\n")
        self.zone_texte.see(tk.END)  # Scroll automatique vers le bas
        self.zone_texte.config(state=tk.DISABLED)

    def traiter_commande(self, event=None):
        """Récupère la commande, l'envoie au jeu, et affiche le résultat."""
        commande = self.entree_commande.get().strip()
        if not commande:
            return

        # Effacer la barre de saisie
        self.entree_commande.delete(0, tk.END)

        # Condition de sortie
        if commande.lower() in ["quitter", "exit", "quit"]:
            self.fenetre.quit()
            return

        # Affichage de la commande tapée par le joueur
        self.ajouter_texte(f"\n> {commande}")
        
        # Exécution dans le moteur et récupération de la réponse
        reponse = self.joueur.executer_commande(commande)
        self.ajouter_texte(reponse)

if __name__ == "__main__":
    racine = tk.Tk()
    app = InterfaceJeu(racine)
    racine.mainloop()