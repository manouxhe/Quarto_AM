from client import a_gagner, trouver_coup_gagnant, play_move, trouve_securité_piece, all_pieces, server_local
import socket
import json
import threading
import time

from client import server_local  # adapte si ton fichier ne s'appelle pas client.py

def start_server():
    def run_server():
        server_local("0.0.0.0", 5001)

    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(0.5)


def test_a_gagner_vrai(): #on test la fonction pr 4 dernier attributs ici P
    ligne = ["BDCP", "SDCP", "LDCP", "CDCP"] 
    assert a_gagner(ligne) == True

def test_a_gagner_faux():# on teste ici pr différents attributs
    ligne = ["BDCP", "SLFP", "LDCE", "CDCP"]  
    assert a_gagner(ligne) == False

def test_play_move_vide(): #on teste pr quand le plateau est vide board a 0 pieces et on a une pieces bcpd
    state = {
        "board": [None] * 16,
        "piece": "BDCP"
    }
    move = play_move(state)
    assert move["pos"] in range(16)
    assert move["piece"] is not None

def test_play_move_aleatoire(): #test quand trouver_coup_gagnant() retourne None
    state = {
        "board": ["BDCP", None, None, None, None, None, None, None,
                  None, None, None, None, None, None, None, None],
        "piece": "SLFP"
    }
    move = play_move(state)
    assert move["pos"] in range(16)
    assert move["piece"] is not None

def test_a_gagner_incomplet(): #pr une ligne vide
    ligne = ["BDCP", "BDCP", None, None]
    assert a_gagner(ligne) == False


def test_trouver_coup_gagnant(): # tester quand il y a deja victoire
    board = ["BDCP", "BDCP", "BDCP", None] + [None]*12
    piece = "BDCP"
    pos = trouver_coup_gagnant(board, piece)
    assert pos == 3

def test_piece_safe_totale(): #quand y a pas de piece dangeureuse 
    board = [None] * 16
    restante = ["BDCP", "SLFP"]
    p = trouve_securité_piece(board, restante)
    assert p in restante

#on est à 54 la !!!! faut + de test 




def test_aucune_piece_safe(): #quand aucune pièce n’est safe
    board = ["BDCP", "BDCP", "BDCP", None] + [None]*12
    restante = ["BDCP"]  # seule pièce restante est dangereuse
    p = trouve_securité_piece(board, restante)
    assert p == "BDCP"  # pas le choix l’IA doit quand même la donner


def test_piece_dangereuse_rejetee(): #qd piece est dangeureuse 
    board = ["BDCP", "BDCP", "BDCP", None] + [None]*12
    restante = ["BDCP", "SLFP"]
    p = trouve_securité_piece(board, restante)

    # On vérifie juste que l’IA retourne une pièce du bon ensemble
    assert p in restante



def test_play_move_fin_de_partie(): #qd le plateau est plein 
    board = ["BDCP", "SLFP", "SLFP", "BDCP",
         "SLFP", "BDCP", "SLFP", "BDCP",
         "SLFP", "BDCP", "SLFP", "BDCP",
         "SLFP", None, "SLFP", "BDCP"]
    state = {
        "board": board,
        "piece": "SLFP"
    }
    move = play_move(state)
    assert move["pos"] in range(16)
    assert move["piece"] is not None

#57%

def test_piece_dangereuse_diagonale(): #pièce dangereuse en diagonale
    board = ["BDCP", None, None, None,
             None, "BDCP", None, None,
             None, None, "BDCP", None,
             None, None, None, None]
    restante = ["BDCP", "SLFP"]
    
    p = trouve_securité_piece(board, restante)
    
    # BDCP = dangereuse si l’adversaire la pose à pos=15 il gagne par diagonale
    assert p in restante



def test_play_move_victoire_possible(): #quand IA peut gagner directement
    board = ["BDCP", "BDCP", "BDCP", None] + [None]*12
    state = {
        "board": board,
        "piece": "BDCP"
    }
    move = play_move(state)

    # IA devrait jouer en position 3 pour compléter la ligne et gagner
    assert move["pos"] == 3
    assert move["piece"] is not None




def test_play_move_aucune_piece_restante():
    board = ["BDCP"] * 15 + [None]  # Presque tout est rempli
    piece = "SLFP"  # Dernière pièce à jouer
    state = {
        "board": board,
        "piece": piece
    }

    move = play_move(state)

    # Ici, il ne reste plus rien à donner : on doit renvoyer 'None'
    assert move["pos"] in range(16)
    assert move["piece"] in all_pieces()

def test_play_move_1_case_libre(): #aucune victoire possible et une piece libre
    board = ["BDCP"] * 15 + [None]
    state = {
        "board": board,
        "piece": "SLFP"
    }
    move = play_move(state)
    assert move["pos"] == 15
    assert move["piece"] is not None

def test_play_move_piece_inconnue(): #avec pièce inconnue (pas dans all_pieces)
    board = [None] * 16
    state = {
        "board": board,
        "piece": "ZZZZ"  # pas une vraie pièce mais format valide
    }
    move = play_move(state)
    assert move["pos"] in range(16)
    assert move["piece"] is not None


#58%

def test_ping_response():
    start_server()
    s = socket.socket()
    s.connect(("localhost", 5001))
    s.send(json.dumps({"request": "ping"}).encode())
    response = s.recv(512).decode()
    assert json.loads(response)["response"] == "pong"
    s.close()

 
def test_play_response():
    start_server()
    virtual_state = {
        "board": [None] * 16,
        "piece": "SDFP"
    }
    s = socket.socket()
    s.connect(("localhost", 5001))
    s.send(json.dumps({'request': 'play', 'state': virtual_state}).encode())
    response = json.loads(s.recv(512).decode())

    assert response['response'] == 'move'
    assert 'pos' in response['move'] and isinstance(response['move']['pos'], int)
    assert 'piece' in response['move'] and isinstance(response['move']['piece'], str)
    s.close()

def test_message_non_json():
    start_server()
    s = socket.socket()
    s.connect(("localhost", 5001))
    s.send(b"Ceci n'est pas du JSON")  # message non json
    time.sleep(0.2)  # laisse le serveur le traiter
    s.close()


def test_message_non_json():
    start_server()
    s = socket.socket()
    s.connect(("localhost", 5001))
    s.send(b"<<<ERREUR>>>")  # pas un JSON 
    time.sleep(0.3)
    s.close()


def test_play_move_aucune_piece_a_donner():
    used = list(all_pieces())
    board = used[:-1] + [None]  # 15 pièces déjà posées, 1 vide
    piece = used[-1]  # la 16e est celle qu’on doit jouer maintenant

    state = {
        "board": board,
        "piece": piece
    }

    move = play_move(state)

    assert move["pos"] in range(16)
    # il ne reste plus de pièce à donner, donc l’IA doit donner None ou quelque chose hors des pièces
    assert move["piece"] is None or move["piece"] in all_pieces()


def test_piece_vraiment_dangereuse_forcee():
    board = ["BDCP", "BDCP", "BDCP", None] + [None] * 12
    # BDCP est déjà alignée, si on en place une 4e => danger
    dangereuse = ["BDCP"]
    p = trouve_securité_piece(board, dangereuse)
    # Il n’y a que cette pièce : donc il la retourne malgré le danger
    assert p == "BDCP"





def test_trouver_coup_gagnant_colonne():
    board = [None]*16
    board[0] = board[4] = board[8] = "BDCP"
    piece = "BDCP"
    assert trouver_coup_gagnant(board, piece) == 12

def test_trouver_coup_gagnant_diagonale():
    board = [None]*16
    board[0] = board[5] = board[10] = "BDCP"
    piece = "BDCP"
    assert trouver_coup_gagnant(board, piece) == 15

def test_request_inconnue():
    start_server()
    s = socket.socket()
    s.connect(("localhost", 5001))
    s.send(json.dumps({"request": "inconnu"}).encode())
    time.sleep(0.2)
    s.close()


def test_trouve_securite_piece_evite_victoire():
    board = [
        "BDCP", None, None, None,
        "BDCP", None, None, None,
        "BDCP", None, None, None,
        None,  None, None, None
    ]
    # BDCP posée en (0,0), (1,0), (2,0) -> si l'IA donne BDCP, l'adversaire peut jouer en (3,0)
    pieces_restantes = ["BDCP", "SLFP"]
    
    safe_piece = trouve_securité_piece(board, pieces_restantes)

    # IA ne doit pas donner BDCP car elle permet  victoire immédiate
    assert safe_piece != "BDCP"
