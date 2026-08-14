import tkinter as tk
from tkinter import scrolledtext
from main import initialiser_jeu  

class InterfaceJeu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("MiamCorp - Aventure Textuelle")
        self.fenetre.geometry("850x500")
        self.fenetre.configure(bg="black")
        
        self.joueur = initialiser_jeu()

        cadre_haut = tk.Frame(fenetre, bg="black")
        cadre_haut.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        cadre_bas = tk.Frame(fenetre, bg="black")
        cadre_bas.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.zone_texte = scrolledtext.ScrolledText(
            cadre_haut, wrap=tk.WORD, bg="black", fg="lightgreen", 
            font=("Courier", 11), state=tk.NORMAL
        )
        self.zone_texte.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.canvas_carte = tk.Canvas(
            cadre_haut, width=200, bg="gray10", highlightthickness=1, highlightbackground="lightgreen"
        )
        self.canvas_carte.pack(side=tk.RIGHT, fill=tk.Y)

        self.ajouter_texte("="*50 + "\n BIENVENUE DANS L'AVENTURE DE LA MORT \n" + "="*50 + "\n")
        self.ajouter_texte(self.joueur.executer_commande("examiner") + "\n")

        self.entree_commande = tk.Entry(
            cadre_bas, font=("Courier", 12), bg="gray15", fg="white", insertbackground="white"
        )
        self.entree_commande.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entree_commande.bind("<Return>", self.traiter_commande)
        self.entree_commande.focus()

        self.bouton_valider = tk.Button(
            cadre_bas, text="Action !", bg="green", fg="white", 
            font=("Courier", 10, "bold"), command=self.traiter_commande
        )
        self.bouton_valider.pack(side=tk.RIGHT)
        
        self.mettre_a_jour_carte()

    def ajouter_texte(self, texte):
        self.zone_texte.config(state=tk.NORMAL)
        self.zone_texte.insert(tk.END, texte + "\n")
        self.zone_texte.see(tk.END)
        self.zone_texte.config(state=tk.DISABLED)

    def traiter_commande(self, event=None):
        commande = self.entree_commande.get().strip()
        if not commande:
            return

        self.entree_commande.delete(0, tk.END)

        if commande.lower() in ["quitter", "exit", "quit"]:
            self.fenetre.quit()
            return

        self.ajouter_texte(f"\n> {commande}")
        
        reponse = self.joueur.executer_commande(commande)
        self.ajouter_texte(reponse)
        
        self.mettre_a_jour_carte()

    def mettre_a_jour_carte(self):
        self.canvas_carte.delete("all")
        
        couleur_active = "lightgreen"
        couleur_inactive = "gray30"
        texte_actif = "black"
        texte_inactif = "gray60"
        
        self.canvas_carte.create_text(100, 20, text="-- PLAN --", fill="lightgreen", font=("Courier", 12, "bold"))
        
        est_bureau = (self.joueur.lieu_actuel.nom == "Bureau Secret")
        self.canvas_carte.create_rectangle(30, 60, 170, 120, fill=couleur_active if est_bureau else couleur_inactive)
        self.canvas_carte.create_text(100, 90, text="Bureau Secret", fill=texte_actif if est_bureau else texte_inactif, font=("Courier", 9, "bold"))
        
        self.canvas_carte.create_line(100, 120, 100, 180, fill="lightgreen", width=2, dash=(4, 2))
        
        est_biblio = (self.joueur.lieu_actuel.nom == "Bibliothèque")
        self.canvas_carte.create_rectangle(30, 180, 170, 240, fill=couleur_active if est_biblio else couleur_inactive)
        self.canvas_carte.create_text(100, 210, text="Bibliothèque", fill=texte_actif if est_biblio else texte_inactif, font=("Courier", 9, "bold"))

if __name__ == "__main__":
    racine = tk.Tk()
    app = InterfaceJeu(racine)
    racine.mainloop()