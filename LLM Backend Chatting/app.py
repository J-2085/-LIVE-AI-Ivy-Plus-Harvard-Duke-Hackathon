from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from flask_cors import CORS
import random
import requests
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

rooms = {}


import time
from flask_socketio import join_room, leave_room, send, SocketIO

# Oyun durumunu tutacak değişkenler
game_time = 15
current_player = 1
total_players = 8
active_players = []
voting_time = 10
game_phase = "speaking"  # speaking veya voting

def initialize_game(room):
    global active_players
    rooms[room]['game_state'] = {}
    rooms[room]['game_state']['active_players'] = list(range(1, total_players + 1))
    rooms[room]['game_state']['game_time'] = 15
    rooms[room]['game_state']['current_player'] = 1
    rooms[room]['game_state']['total_players'] = 8
    rooms[room]['game_state']['voting_time'] = 10
    rooms[room]['game_state']['game_phase'] = "waiting"  # waiting, speaking veya voting



def game_loop(room):
    global game_state
    # Minimum oyuncu sayısı kontrolü

    initialize_game(room)

    while rooms[room]["members"] < 2:
        print(f"Waiting for players... Current count: {rooms[room]['members']}")
        socketio.emit('update_game', {
            'speaker': None,
            'time_left': 100,
            'phase': 'waiting',
            'active_players': [],
        }, room=room)
        time.sleep(1)

        print(rooms)
    
    print("Enough players joined, starting game...")
    
    game_state = rooms[room]['game_state']

    set_play_ids(room)


    print(rooms[room]["players"], "test play ids")

    while len(game_state['active_players']) > 1:


        print(rooms)
        # Konuşma fazı
        game_state['game_phase'] = "speaking"
        for game_state['current_player'] in game_state['active_players'] :


            game_state['game_time'] = 5


            print(rooms[room]['messages'], "messages")
            

            player_ids = [player['player_id'] for player in rooms[room]["players"]]
            if not (game_state['current_player'] in player_ids):
                 # Yapay zeka mesajı için rastgele bekleme
                if rooms[room]['mode'] == "red":
                    response = get_ai_talk(rooms[room]['messages'],"red")
                else:
                    response = get_ai_talk(rooms[room]['messages'],"blue")

                content = {
                "name": f"Karakter {game_state['current_player']}",
                "message": response
                }

                time.sleep(random.randint(1, 13)) 
                rooms[room]["messages"].append(content)

                socketio.emit("recMessage", {"content": content, "message": "massage received"}, room=room)
            #response şimdi frontende aktar



            while game_state['game_time'] > 0:
                print(f"Game time: {game_state['game_time']}")
                print(f"Current player: {game_state['current_player']}")
                socketio.emit('update_game', {
                    'phase': game_state['game_phase'],
                    'speaker': game_state['current_player'],
                    'time_left': game_state['game_time'],
                    'active_players': game_state['active_players'],
                    'player_list': rooms[room]['players']
                }, room=room)
                game_state['game_time'] -= 1
                time.sleep(1)
        
        # Oylama fazı
        game_state['game_phase'] = "voting"
        game_state['voting_time'] = 10
        game_state['votes'] = {}  # Her oyuncunun aldığı oyları tutacak
        
        # Oylama başladı sinyali
        socketio.emit('update_game', {
            'phase': game_state['game_phase'],
            'time_left': game_state['voting_time'],
            'active_players': game_state['active_players'],
            'player_list': rooms[room]['players']
        }, room=room)
        
        
        for player in game_state['active_players']:
            # Geçici olarak mevcut oyuncuyu listeden çıkar
            temp_active_players = game_state['active_players'].copy()
            temp_active_players.remove(player)

            player_ids = [player['player_id'] for player in rooms[room]["players"]]

            print("MADDE 4: ",game_state['current_player'] in player_ids)

            if not (player in player_ids):

                if rooms[room]['mode'] == "red":
                    response = get_ai_vote(rooms[room]['messages'], temp_active_players, "red")
                else:
                    response = get_ai_vote(rooms[room]['messages'], temp_active_players, "blue")


                print(player, "player", game_state['active_players'], "active players", response, "response")


                number = int(re.search(r'\d+', response).group())

                print(number, "number")

                print(game_state['votes'] , "before")
                print(game_state['game_phase'] == "voting" , "game phase")
                print(player in game_state['active_players'] , "player in active players")
                print(number in game_state['active_players'] , "number in active players")

                if game_state['game_phase'] == "voting" and player in game_state['active_players'] and number in game_state['active_players']:
                    game_state['votes'][number] = game_state['votes'].get(number, 0) + 1
                    print(game_state['votes'],"after")
        


        while game_state['voting_time'] > 0:
            socketio.emit('update_voting_time', {
                'time_left': game_state['voting_time']
            }, room=room)
            game_state['voting_time'] -= 1
            time.sleep(1)
        
        # Oyları topla ve sonucu değerlendir
        eliminated_player = handle_voting_results(game_state['votes'])
        if eliminated_player in game_state['active_players']:
            game_state['active_players'].remove(eliminated_player)

        


        socketio.emit('player_eliminated', {
            'eliminated_player': eliminated_player,
            'remaining_players': game_state['active_players']
        }, room=room)

        print(game_state['active_players'])
        player_ids = [player['player_id'] for player in rooms[room]["players"]]
        
        # Eğer tüm aktif oyuncular AI ise veya gerçek oyuncu kalmadıysa oyunu bitir
        if (set(game_state['active_players']) == set(player_ids)) or not any(pid in game_state['active_players'] for pid in player_ids):
            break
        
        time.sleep(2)  # Sonuçları göstermek için kısa bir bekleme
    
    # Oyun bitti, kazanan belirlendi

    if (set(game_state['active_players']) == set(player_ids)):
        socketio.emit('game_ended', {
            'winner': "Humans"
        }, room=room)
        print("game ended ", rooms)
    else:
        socketio.emit('game_ended', {
            'winner': "AIs"
        }, room=room)
        print("game ended ", rooms)
    del rooms[room]

    print("game ended after delete", rooms)



def handle_voting_results(votes):
    # En çok oy alan oyuncuyu belirle
    if not game_state['votes']:
        return game_state['active_players'][0]  # Test için, gerçek implementasyonda değişecek
    
    max_votes = max(game_state['votes'].values())
    most_voted = [player for player, vote_count in game_state['votes'].items() if vote_count == max_votes]
    return most_voted[0]

def set_play_ids(room):
    numbers = set()
    for player in rooms[room]["players"]:
        while True:
            number = random.randint(1, 8)
            if number not in numbers:
                numbers.add(number)
                player["player_id"] = number
                break



def get_ai_talk(messages,mode):

    talk_meta = ""
    if mode == "red":
        talk_meta = "https://llm-backend-ibm-759420319197.us-central1.run.app/ai/red_chat"
    else:
        talk_meta = "https://llm-backend-ibm-759420319197.us-central1.run.app/ai/blue_chat"
    
    
    conversation_history = [f"{msg['name']}: {msg['message']}" for msg in messages] 
  
    payload = {
        "prompt": f"Oyundaki rolüne göre konuşma yap {conversation_history}"  # Buraya istediğiniz promptu ekleyebilirsiniz
    }
    
    print(payload, "payload")

    try:
        response = requests.post(talk_meta, json=payload)

        print(response.content, "response")

        return str(clean_byte_string(response.content))  # API'nin döndürdüğü yanıt formatına göre ayarlayın
        
    except requests.exceptions.RequestException as e:
        print(f"AI sistemi ile iletişim hatası: {e}")
        return "Üzgünüm, şu anda yanıt üretemiyorum."

def get_ai_vote(messages,active_list,mode):
    
    
    vote_meta = ""
    if mode == "red":
        vote_meta = "https://llm-backend-ibm-759420319197.us-central1.run.app/ai/red_vote"
    else:
        vote_meta = "https://llm-backend-ibm-759420319197.us-central1.run.app/ai/blue_vote"
    
    conversation_history = [f"{msg['name']}: {msg['message']}" for msg in messages] 
  

    print("active_list", active_list)
    payload = {
        "prompt": f"Mesaj geçmişi: {conversation_history}",
        "active_list": active_list
    }

    try:
        response = requests.post(vote_meta, json=payload)
        print(response.content, "response")
        return str(response.content)
    except requests.exceptions.RequestException as e:
        print(f"AI sistemi ile iletişim hatası: {e}")
        return "Üzgünüm, şu anda oy üretemiyorum."

@socketio.on("submit_vote")
def handle_vote(data):
    voter = data.get("voter")
    voted_for = data.get("voted_for")
    room = data.get("room")
    
    print("Vote had been submitted")
    print(voter, voted_for, room)

    print(game_state['game_phase'] == "voting" , "game phase")
    print(voter in game_state['active_players'] , "voter in active players")
    print(voter)
    print(game_state['active_players'])
    print(voted_for in game_state['active_players'] , "voted for in active players")

    if game_state['game_phase'] == "voting" and voter in game_state['active_players'] and voted_for in game_state['active_players']:
        # Oyu kaydet
        print("if state worked")
        game_state['votes'][voted_for] = game_state['votes'].get(voted_for, 0) + 1
        socketio.emit('vote_registered', {
            'voter': voter
        }, room=room)

    print(game_state['votes'])   

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        json_data = request.get_json()
        name = json_data.get("name")
        code = json_data.get("code")
        join = json_data.get("join", False)
        create = json_data.get("create", False)
        mode = json_data.get("mode")
        print(name, create, mode)


        if not name:
            return jsonify({"error": "Name is required"}), 400
        if not mode:
            return jsonify({"error": "Mode is required"}), 400
        if join != False and not code:
            return jsonify({"error": "Room code is required"}), 400
 
        
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": [], "players": [], "mode": mode}


            socketio.start_background_task(target=game_loop, room=room)
            return jsonify({"room": room}), 200
        
        if join != False and code in rooms:
            room = code
            return jsonify({"room": room}), 200

        return jsonify({"error": "Invalid request"}), 400

    return jsonify({"error": "Invalid request"}), 400


@app.route("/get-ai-response", methods=["POST"])
def get_ai_response():
    data = request.get_json()
    print("Message received: ", data)
    print("Room: ", data["room"])
    print("Rooms", rooms)
    room = data["room"]
    if room not in rooms:
        return 
    
    content = {
        "name": data["name"],
        "message": data["data"]
    }
    
    rooms[room]["messages"].append(content)
    
    socketio.emit("recMessage", {"content": content, "message": "massage received"}, room=room)
    

    print("Message added to room ")
    
    print(f"{data["name"]} said: {data['data']}")
    return jsonify({"message": "AI response received"}), 200

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return jsonify({"code": room, "messages": rooms[room]["messages"]}), 200

@socketio.on("newMessage")
def message(data):
    print("Message received: ", data)
    print("Room: ", data["room"])
    print("Rooms", rooms)
    room = data["room"]
    if room not in rooms:
        return 
    
    content = {
        "name": data["name"],
        "message": data["data"]
    }
  
    rooms[room]["messages"].append(content)
    
   
    send({"content": content, "message": "massage received"}, to=room)
    print("Message added to room ")
    
    print(f"{data["name"]} said: {data['data']}")

    return jsonify({"message": "AI response received"}), 200

@socketio.on("connect")
def connect(auth):
    print("Connected: from React")
    

@socketio.on("joinRoom")
def joinRoom(data):
    print(data, "joinRoom data")
    room = data.get("room")
    name = data.get("name")
    mode = data.get("mode")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    


    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1

    player = {"player_name": name, "player_id": 0}

    rooms[room]["players"].append(player)
    

    print(f"{name} joined room {room}")


@socketio.on("leaveRoom")
def leaveRoom(auth):
    json_data = request.get_json()
    room = json_data.get("room")
    name = json_data.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")
    


@socketio.on("disconnect")
def disconnect():
    print("Disconnected: from React")



def clean_byte_string(byte_str):
    if isinstance(byte_str, bytes):
        # Bytes'i decode edip, baştaki ve sondaki gereksiz boşlukları ve tırnakları temizle
        return byte_str.decode('utf-8').strip().strip('"')
    return byte_str  # Eğer zaten string ise, olduğu gibi döndür


if __name__ == "__main__":
    
    socketio.run(app,host="0.0.0.0",port=5000, debug=True)
    