import unittest
from monde import Lieu, Objet, MemoireMonde, ActionInvalideError
from moteur import Joueur

class TestMoteurJeu(unittest.TestCase):
    
    def setUp(self):
        """Initialisation d'un environnement de test isolé avant chaque fonction de test."""
        self.memoire = MemoireMonde()
        self.salle_depart = Lieu("Entrée", "Une petite entrée vide.")
        self.couloir = Lieu("Couloir", "Un long couloir sombre.")
        
        self.salle_depart.ajouter_sortie("nord", self.couloir)
        
        self.parchemin = Objet("Parchemin", "Un vieux bout de papier.")
        self.salle_depart.ajouter_objet(self.parchemin)
        
        self.joueur = Joueur(self.salle_depart, self.memoire)

    def test_deplacement_valide(self):
        """Test que le joueur se déplace bien s'il y a une sortie."""
        self.joueur._aller("nord")
        self.assertEqual(self.joueur.lieu_actuel.nom, "Couloir")

    def test_deplacement_mur(self):
        """Test que le joueur lève bien une ActionInvalideError s'il va dans un mur (Direction sans sortie)."""
        with self.assertRaises(ActionInvalideError):
            self.joueur._aller("sud")

    def test_prendre_objet(self):
        """Test que l'inventaire s'incrémente bien et que le lieu se vide quand on prend un objet."""
        self.joueur._prendre("Parchemin")
        
        self.assertIsNotNone(self.joueur.possede_objet("Parchemin"))
        self.assertEqual(len(self.joueur.inventaire), 1)
        self.assertEqual(len(self.salle_depart.objets), 0)

    def test_memoire_actions_a_fait(self):
        """Test que le système de mémoire (a_fait) fonctionne correctement après une action."""
        self.assertFalse(self.memoire.a_fait("pris_Parchemin"))
        
        self.joueur._prendre("Parchemin")
        
        self.assertTrue(self.memoire.a_fait("pris_Parchemin"))

if __name__ == '__main__':
    unittest.main()