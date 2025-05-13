from client import play_move, all_pieces  # si ton code est dans client.py (sinon remplace par le bon nom)

# cree un plateau vide (aucune pièce posée)
plateau_test = [None] * 16

# choisis  pièce exis a tester 
piece_reçue = "BDCP"  

# Simule etat envoye par le serveur
etat_simulé = {
    "board": plateau_test,
    "piece": piece_reçue
}

# Appelle la fonction de ton IA
coup = play_move(etat_simulé)

# Affiche le résultat
print("Coup joué par IA :")
print(" Position jouée :", coup["pos"])
print(" Piece donnée :", coup["piece"])
