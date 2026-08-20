import tkinter as tk
from tkinter import scrolledtext
import re
from main import initialiser_jeu  

class InterfaceJeu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("MiamCorp - L'Éveil de la Relique")
        self.fenetre.geometry("850x550")
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

        commande = re.sub(r'\s+', ' ', commande)

        self.entree_commande.delete(0, tk.END)

        if commande.lower() in ["quitter", "exit", "quit"]:
            self.fenetre.quit()
            return

        self.ajouter_texte(f"\n> {commande}")
        
        reponse = self.joueur.executer_commande(commande)
        self.ajouter_texte(reponse)
        
        self.mettre_a_jour_carte()
        if self.joueur.possede_objet("Relique"):
            if self.joueur.memoire.a_fait("chien_mort"):
                self.declencher_fin_mauvaise()
            else:
                self.declencher_fin()

    def declencher_fin(self):
        self.ajouter_texte("\n" + "="*50)
        self.ajouter_texte(" FÉLICITATIONS !")
        self.ajouter_texte(" Vous avez mis la main sur la Relique Maudite.")
        self.ajouter_texte(" Les murs tremblent, la malédiction de la MiamCorp est levée !")
        self.ajouter_texte(" --- FIN DU JEU ---")
        self.ajouter_texte("="*50)
        self.entree_commande.config(state=tk.DISABLED)
        self.bouton_valider.config(state=tk.DISABLED)

    def declencher_fin_mauvaise(self):
        self.ajouter_texte("\n" + "="*50)
        self.ajouter_texte(" LA COLÈRE DU GARDIEN S'ABAT SUR VOUS !")
        self.ajouter_texte(" Alors que vous saisissez la Relique avec triomphe, une ombre surgit dans votre dos.")
        self.ajouter_texte(" C'est le Gardien. Le visage déformé par une haine pure, il vous poignarde à de multiples reprises.")
        self.ajouter_texte(" « Ça, c'est pour mon chien... » murmure-t-il alors que votre vue s'obscurcit à jamais.")
        self.ajouter_texte(" VOUS ÊTES MORT.")
        self.ajouter_texte(" --- FIN DU JEU (MAUVAISE FIN) ---")
        self.ajouter_texte("="*50)
        self.entree_commande.config(state=tk.DISABLED)
        self.bouton_valider.config(state=tk.DISABLED)
        self.fenetre.after(14000, lambda: self.fenetre.quit())

    def mettre_a_jour_carte(self):
        self.canvas_carte.delete("all")
        
        couleur_active = "lightgreen"
        couleur_inactive = "gray30"
        texte_actif = "black"
        texte_inactif = "gray60"
        
        self.canvas_carte.create_text(100, 20, text="-- PLAN --", fill="lightgreen", font=("Courier", 12, "bold"))
        
        est_bureau = (self.joueur.lieu_actuel.nom == "Bureau Secret")
        self.canvas_carte.create_rectangle(30, 50, 170, 90, fill=couleur_active if est_bureau else couleur_inactive)
        self.canvas_carte.create_text(100, 70, text="Bureau Secret", fill=texte_actif if est_bureau else texte_inactif, font=("Courier", 9, "bold"))
        
        self.canvas_carte.create_line(100, 90, 100, 130, fill="lightgreen", width=2, dash=(4, 2))
        
        est_biblio = (self.joueur.lieu_actuel.nom == "Bibliothèque")
        self.canvas_carte.create_rectangle(30, 130, 170, 170, fill=couleur_active if est_biblio else couleur_inactive)
        self.canvas_carte.create_text(100, 150, text="Bibliothèque", fill=texte_actif if est_biblio else texte_inactif, font=("Courier", 9, "bold"))

        self.canvas_carte.create_line(100, 170, 100, 210, fill="lightgreen", width=2, dash=(4, 2))

        est_couloir = (self.joueur.lieu_actuel.nom == "Couloir Sombre")
        self.canvas_carte.create_rectangle(30, 210, 170, 250, fill=couleur_active if est_couloir else couleur_inactive)
        self.canvas_carte.create_text(100, 230, text="Couloir Sombre", fill=texte_actif if est_couloir else texte_inactif, font=("Courier", 9, "bold"))

        self.canvas_carte.create_line(100, 250, 100, 290, fill="lightgreen", width=2, dash=(4, 2))

        est_crypte = (self.joueur.lieu_actuel.nom == "Crypte")
        self.canvas_carte.create_rectangle(30, 290, 170, 330, fill=couleur_active if est_crypte else couleur_inactive)
        self.canvas_carte.create_text(100, 310, text="Crypte", fill=texte_actif if est_crypte else texte_inactif, font=("Courier", 9, "bold"))
        
if __name__ == "__main__":
    racine = tk.Tk()
    app = InterfaceJeu(racine)
    racine.mainloop()