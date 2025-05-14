from client import play_move, all_pieces  

# cree un plateau vide (aucune pièce posée)
plateau_test = [None] * 16

# choisis  pièce exis a tester 
piece_reçue = "BDCP"  

# Simule etat envoye par le serveur
etat_simulé = {
    "board": plateau_test,
    "piece": piece_reçue
}

coup = play_move(etat_simulé)

print("Coup joué par IA :")
print(" Position jouée :", coup["pos"])
print(" Piece donnée :", coup["piece"])
