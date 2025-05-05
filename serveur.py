import socket
import json
import threading

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
                    # Exemple simple de réponse (à adapter avec ta logique)
                    move = get_next_move()
                    response = {
                        "response": "move",
                        "move": move,
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
        
        
def get_next_move():
    # logique de jeu ici
    # Pour l'instant on retourne un move fictif
    return ""  # ou une valeur calculée


        
if __name__ == "__main__":
    inscription_server()
    server_local("0.0.0.0", 5001)
    client()
    
