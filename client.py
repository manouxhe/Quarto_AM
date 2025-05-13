import socket
import json
import random
 
 #Le serveur (le prof) est sur cette adresse IP et ce port on se connecte là pour s’inscrire au tournoi
def inscription_server():   
    server = '192.168.129.15'  # Adressse ip du serveur
    port = 3000       # Port du serveur auquel on se connecte


    message = {   #message d’inscription à envoyer au prof :
        "request": "subscribe",
        "port": 5001,
        "name": "AYOUBQUARTOOOOO",
        "matricules": ["12345", "67890"]
    }

    message_str = json.dumps(message)  #transformes le message JSON en texte brut puis en bytes pour l’envoyer par le réseau
    message_bytes = message_str.encode()

    # Création du socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: # Connexion avec le serveur
        client_socket.connect((server, port))
        print("Connecté au serveur.")

        # Envoi du message d’inscription au tournoi
        client_socket.sendall(message_bytes)  
        print("Message envoyé au serveur.")

        # Boucle de réception des messages
        while True:
            data = client_socket.recv(4096) # Attente des messages du serveur (genre confirmation ou infos)
            if not data:
                print("Connexion fermée par le serveur.")
                break
            print("Message reçu :", data.decode())

    except Exception as e:
        print("Erreur :", e)
    finally:
        client_socket.close()
        
    

# propre serveur local qui va écouter les messages du prof 
def server_local(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen() #prêt à écouter les connexions

    print(f"Serveur local est en écoute sur le port {port}...")

    while True:
        conn, addr = server_socket.accept()  #chaque fois qu’un message du tournoi arrive on accepte la connexion entrante
        print(f"Connexion entrante depuis {addr}")
        client(conn, addr)
       # threading.Thread(target= client, args=(conn, addr)).start()

def client(conn, addr): # fonction est lancée à chaque message reçu s’occupe de lire analyser et répondre au message
    try:
        while True:
            data = conn.recv(4096) # lis ce que le serveur t’a envoyé (jusqu’à 4096 octets).
            if not data:
                break

            message = data.decode()
            print(f"Message reçu de {addr} : {message}")

            try:
                json_data = json.loads(message) # convertis le message en texte, puis en dictionnaire Python (grâce à json.loads).
                requete = json_data.get("request") #regardes le type de message envoyé par le serveur
                
                 #"ping" → test de connexion
                 #"play" → c’est à toi de jouer

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
                    pieces.add(piece) #Tu ajoutes cette pièce dans l’ensemble.
    return pieces #La fonction retourne l’ensemble complet des 16 pièces du jeu.

def play_move(state):
    board = state["board"]
    current_piece = state["piece"]

    vide_positions = [i for i, cell in enumerate(board) if cell is None]
    utilisé_pieces = {p for p in board if p is not None}
    utilisé_pieces.add(current_piece)

    all_pieces = all_pieces()
    restante_pieces = list(all_pieces - utilisé_pieces)

    # 1. Chercher un coup gagnant
    if trouver_coup_gagnant(board, current_piece) is not None:
        chosen_pos = trouver_coup_gagnant(board, current_piece)
    else:
        chosen_pos = random.choice(vide_positions)

    # 2. Donner une pièce safe à l’adversaire
    chosen_piece = trouve_securité_piece(board, restante_pieces)

    return {
        "pos": chosen_pos,
        "piece": chosen_piece
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

def trouve_securité_piece(board, restante_pieces):
    securité_pieces = []

    for piece in restante_pieces:
        safe = True
        for i in range(16):
            if board[i] is None:
                temp_board = board.copy()
                temp_board[i] = piece

                # reconstruction du plateau
                grid = [temp_board[j*4:(j+1)*4] for j in range(4)]

                # tester lignes
                for ligne in grid:
                    if a_gagner(ligne):
                        safe = False
                        break
                # colonnes
                if safe:
                    for col in range(4):
                        colonne = [grid[row][col] for row in range(4)]
                        if a_gagner(colonne):
                            safe = False
                            break
                # diagonales
                if safe:
                    diag1 = [grid[d][d] for d in range(4)]
                    diag2 = [grid[d][3 - d] for d in range(4)]
                    if a_gagner(diag1) or a_gagner(diag2):
                        safe = False

                if not safe:
                    break

        if safe:
            securité_pieces.append(piece)

    if securité_pieces:
        return random.choice(securité_pieces)
    else:
        return random.choice(restante_pieces)
   

        
if __name__ == "__main__":
    inscription_server()
    server_local("0.0.0.0", 5001)
    client()
    
    