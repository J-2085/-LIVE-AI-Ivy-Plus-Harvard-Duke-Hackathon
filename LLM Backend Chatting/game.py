# from flask import Flask, render_template, request, session, redirect, url_for, jsonify
# from flask_socketio import join_room, leave_room, send, SocketIO
# import random
# from string import ascii_uppercase
# from flask_cors import CORS
# from game import game_loop
# import threading

# app = Flask(__name__)
# app.config["SECRET_KEY"] = "hjhjsdahhds"
# socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)

# rooms = {}


# import time
# from flask_socketio import join_room, leave_room, send, SocketIO

# # Oyun durumunu tutacak değişkenler
# game_time = 15
# current_player = 1
# total_players = 8
# active_players = []
# voting_time = 10
# game_phase = "speaking"  # speaking veya voting

# def initialize_game():
#     global active_players
#     active_players = list(range(1, total_players + 1))

# def game_loop():
#     global game_time, current_player, game_phase, active_players, votes
#     initialize_game()
    
#     while len(active_players) > 1:
#         # Konuşma fazı
#         game_phase = "speaking"
#         for current_player in active_players:
#             game_time = 1
#             while game_time > 0:
#                 print(f"Game time: {game_time}")
#                 print(f"Current player: {current_player}")
#                 socketio.emit('update_game', {
#                     'phase': game_phase,
#                     'speaker': current_player,
#                     'time_left': game_time,
#                     'active_players': active_players
#                 })
#                 game_time -= 1
#                 time.sleep(1)
        
#         # Oylama fazı
#         game_phase = "voting"
#         voting_time = 1
#         votes = {}  # Her oyuncunun aldığı oyları tutacak
        
#         # Oylama başladı sinyali
#         socketio.emit('update_game', {
#             'phase': game_phase,
#             'time_left': voting_time,
#             'active_players': active_players
#         })
        
#         while voting_time > 0:
#             socketio.emit('update_voting_time', {
#                 'time_left': voting_time
#             })
#             voting_time -= 1
#             time.sleep(1)
        
#         # Oyları topla ve sonucu değerlendir
#         eliminated_player = handle_voting_results(votes)
#         if eliminated_player in active_players:
#             active_players.remove(eliminated_player)

#         print(active_players)


#         socketio.emit('player_eliminated', {
#             'eliminated_player': eliminated_player,
#             'remaining_players': active_players
#         })
        
#         time.sleep(2)  # Sonuçları göstermek için kısa bir bekleme
    
#     # Oyun bitti, kazanan belirlendi
#     socketio.emit('game_ended', {
#         'winner': active_players[0]
#     })

# def handle_voting_results(votes):
#     # En çok oy alan oyuncuyu belirle
#     if not votes:
#         return active_players[0]  # Test için, gerçek implementasyonda değişecek
    
#     max_votes = max(votes.values())
#     most_voted = [player for player, vote_count in votes.items() if vote_count == max_votes]
#     return most_voted[0]

# # Oylama için yeni bir Socket.IO event handler
# @socketio.on("submit_vote")
# def handle_vote(data):
#     voter = data.get("voter")
#     voted_for = data.get("voted_for")
#     room = data.get("room")
    
#     print(voter, voted_for, room)

    

#     if game_phase == "voting" and voter in active_players and voted_for in active_players:
#         # Oyu kaydet
#         votes[voted_for] = votes.get(voted_for, 0) + 1
#         socketio.emit('vote_registered', {
#             'voter': voter
#         }, room=room)

#     print(votes)   

# def generate_unique_code(length):
#     while True:
#         code = ""
#         for _ in range(length):
#             code += random.choice(ascii_uppercase)
        
#         if code not in rooms:
#             break
    
#     return code

# @app.route("/", methods=["POST", "GET"])
# def home():
#     session.clear()
#     if request.method == "POST":
#         json_data = request.get_json()
#         name = json_data.get("name")
#         code = json_data.get("code")
#         join = json_data.get("join", False)
#         create = json_data.get("create", False)

#         print(name, create)


#         if not name:
#             return jsonify({"error": "Name is required"}), 400

#         if join != False and not code:
#             return jsonify({"error": "Room code is required"}), 400
 
        
        
#         if create != False:
#             room = generate_unique_code(4)
#             rooms[room] = {"members": 0, "messages": []}
#             return jsonify({"room": room}), 200
        
#         if join != False and code in rooms:
#             room = code
#             return jsonify({"room": room}), 200

#         return jsonify({"error": "Invalid request"}), 400

#     return jsonify({"error": "Invalid request"}), 400


# @app.route("/get-ai-response", methods=["POST"])
# def get_ai_response():
#     data = request.get_json()
#     print("Message received: ", data)
#     print("Room: ", data["room"])
#     print("Rooms", rooms)
#     room = data["room"]
#     if room not in rooms:
#         return 
    
#     content = {
#         "name": data["name"],
#         "message": data["data"]
#     }
#     #send(content)
#     rooms[room]["messages"].append(content)
    
#     socketio.emit("recMessage", {"content": content, "message": "massage received"}, room=room)
#     #send({"content": content, "message": "massage received"}, to=room)

#     print("Message added to room ")
    
#     print(f"{data["name"]} said: {data['data']}")
#     return jsonify({"message": "AI response received"}), 200

# @app.route("/room")
# def room():
#     room = session.get("room")
#     if room is None or session.get("name") is None or room not in rooms:
#         return redirect(url_for("home"))

#     return jsonify({"code": room, "messages": rooms[room]["messages"]}), 200

# @socketio.on("newMessage")
# def message(data):
#     print("Message received: ", data)
#     print("Room: ", data["room"])
#     print("Rooms", rooms)
#     room = data["room"]
#     if room not in rooms:
#         return 
    
#     content = {
#         "name": data["name"],
#         "message": data["data"]
#     }
#     #send(content)
#     rooms[room]["messages"].append(content)
    
#     #socketio.emit('receiveMessage', content, room=room)
#     send({"content": content, "message": "massage received"}, to=room)
#     print("Message added to room ")
    
#     print(f"{data["name"]} said: {data['data']}")

#     return jsonify({"message": "AI response received"}), 200

# @socketio.on("connect")
# def connect(auth):
#     print("Connected: from React")
    

# @socketio.on("joinRoom")
# def joinRoom(data):
#     print(data, "joinRoom data")
#     room = data.get("room")
#     name = data.get("name")
#     if not room or not name:
#         return
#     if room not in rooms:
#         leave_room(room)
#         return
    
#     join_room(room)
#     send({"name": name, "message": "has entered the room"}, to=room)
#     rooms[room]["members"] += 1
#     print(f"{name} joined room {room}")


# @socketio.on("leaveRoom")
# def leaveRoom(auth):
#     json_data = request.get_json()
#     room = json_data.get("room")
#     name = json_data.get("name")
#     leave_room(room)

#     if room in rooms:
#         rooms[room]["members"] -= 1
#         if rooms[room]["members"] <= 0:
#             del rooms[room]
    
#     send({"name": name, "message": "has left the room"}, to=room)
#     print(f"{name} has left the room {room}")
    


# @socketio.on("disconnect")
# def disconnect():
#     print("Disconnected: from React")

# if __name__ == "__main__":
#     socketio.start_background_task(target=game_loop)
#     socketio.run(app, debug=True)
    