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
    board = state["board"]
    current_piece = state["piece"]

    # Étape 1 : positions libres
    vide_positions = [i for i, cell in enumerate(board) if cell is None]

    # Étape 2 : pièces utilisées
    utilisé_pieces = {piece for piece in board if piece is not None}
    utilisé_pieces.add(current_piece)

    # Étape 3 : pièces restantes
    all_pieces = all_pieces()
    restante_pieces = list(all_pieces - utilisé_pieces)

    # Étape 4 : choisir un coup aléatoire
    choisir_pos = random.choice(vide_positions)
    choisir_piece = random.choice(restante_pieces) if restante_pieces else None

    return {
        "pos": choisir_pos,
        "piece": choisir_piece
    }

    

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
    
    