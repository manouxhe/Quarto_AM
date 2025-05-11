import socket
import json
import threading
import random

def inscription_server():
    # Configuration du serveur
    server = '192.168.129.15' 
    port = 3000       # Port du serveur auquel on se connecte


    message = {
        "request": "subscribe",
        "port": 5001,
        "name": "fun_name_for_the_client",
        "matricules": ["12345", "67890"]
    }


    message_str = json.dumps(message)
    message_bytes = message_str.encode()

    # Création du socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server, port))
        print("Connecté au serveur.")

        # Envoi du message
        client_socket.sendall(message_bytes)
        print("Message envoyé au serveur.")

        # Boucle de réception des messages
        while True:
            data = client_socket.recv(4096)
            if not data:
                print("Connexion fermée par le serveur.")
                break
            print("Message reçu :", data.decode())

    except Exception as e:
        print("Erreur :", e)
    finally:
        client_socket.close()
        
    


def server_local(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Serveur local est en écoute sur le port {port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connexion entrante depuis {addr}")
        threading.Thread(target= client, args=(conn, addr)).start()

def client(conn, addr):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            message = data.decode()
            print(f"Message reçu de {addr} : {message}")

            try:
                json_data = json.loads(message)
                requete = json_data.get("request")
                

                if requete == "ping":
                    response = {"response": "pong"}
                    conn.sendall(json.dumps(response).encode())

                elif requete == "play":
                    state = json_data["state"]
                    move = play_move(state)
                    response = {
                        "response": "move",
                        "move": {"pos": move["pos"],
                        "piece": move["piece"]},
                        "message": "fun"
                    }
                    conn.sendall(json.dumps(response).encode())

                else:
                    print("Requête inconnue :", requete)

            except json.JSONDecodeError:
                print("Message non reconnu comme JSON.")
    except Exception as e:
        print(f"Erreur avec {addr} :", e)
    finally:
        conn.close()
        print(f"Connexion fermée avec {addr}")
    
        

def all_pieces():
    pieces = set()
    for size in ["B", "S"]:
        for color in ["D", "L"]:
            for filling in ["E", "F"]:
                for shape in ["C", "P"]:
                    piece = size + color + filling + shape
                    pieces.add(piece)
    return pieces

def play_move(state):
    board = state["board"] #récupere le plateau actuel envoyé par le serveur
    current_piece = state["piece"] # récupere la pièce que l’adversaire t’a donnée et que tu dois jouer maintenant



    # cas si y a des pieces
    position_gagnante = trouver_coup_gagnant(board, current_piece) #on reg si peut gagner en posant cette pièce qq part

    if position_gagnante is not None:
        # pcs déjà utilisées (sur le plateau + celle qu’on va poser)
        pieces_utilisées = {piece for piece in board if piece is not None}
        pieces_utilisées.add(current_piece)

        # pieces restantes à choisir pour l’adversaire
        toutes_les_pieces = all_pieces()
        pieces_restantes = list(toutes_les_pieces - pieces_utilisées)
        piece_donnee = random.choice(pieces_restantes) if pieces_restantes else None

        return {
            "pos": position_gagnante,
            "piece": piece_donnee
        }

    # 2. Snn jouer au hasard
    positions_vides = [i for i, case in enumerate(board) if case is None]

    # mm calcul des pièces restantes
    pieces_utilisées = {piece for piece in board if piece is not None}
    pieces_utilisées.add(current_piece)
    toutes_les_pieces = all_pieces()
    pieces_restantes = list(toutes_les_pieces - pieces_utilisées)
    
    position_aleatoire = random.choice(positions_vides)
    piece_donnee = random.choice(pieces_restantes) if pieces_restantes else None

    return {
        "pos": position_aleatoire,
        "piece": piece_donnee
    }

def trouver_coup_gagnant(board, piece):
    
    for i in range(16):
        if board[i] is None: #donc si l'endroit est vide 
            plateau_temp = board.copy() #on fait un faux plateau pour simuler si ca va gagner ou pas le coup
            plateau_temp[i] = piece #on place la piece la ou ya  le vide 

            # On reconstruit le plateau en 4x4
            plateau_2d = [plateau_temp[j*4:(j+1)*4] for j in range(4)] #pr travailler avec les lignes colones et diagonales

            # Vérifie lignes dabord puis colonnes puis diagonales
            for ligne in plateau_2d:
                if a_gagner(ligne):
                    return i

            for col in range(4):
                colonne = [plateau_2d[row][col] for row in range(4)]
                if a_gagner(colonne):
                    return i

            diag1 = [plateau_2d[d][d] for d in range(4)]
            diag2 = [plateau_2d[d][3 - d] for d in range(4)]
            if a_gagner(diag1) or a_gagner(diag2):
                return i

    return None

    

def a_gagner(ligne):
    """
    check si les 4 pièces d'une ligne ont un mm attribut cracterstique 
    chaque pièce est une chaîne comme "BDCP" (ex : Grande, Foncée, Pleine, Carrée).
    """
    if None in ligne:
        return False #si y a que 3 pieces doffice c ps gagné

    # on parcourt les 4 attributs possibles des pièces
    for i in range(4):  # 4 attributs
        attributs = [piece[i] for piece in ligne]
        if all(a == attributs[0] for a in attributs):
            return True  # attribut commun 

    return False #snn

        
if __name__ == "__main__":
    inscription_server()
    server_local("0.0.0.0", 5001)
    client()
    
    