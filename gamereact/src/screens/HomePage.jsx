import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import socket from '../services/socket';

function HomePage() {
    const [playerName, setPlayerName] = useState('');
    const [roomCode, setRoomCode] = useState('');
    const navigate = useNavigate();
    const { state } = useLocation();
    const mode = state?.mode;

    console.log(mode, "mode");
    
    const CREATE_ROOM_URL = "https://game-backend-759420319197.us-central1.run.app";

    const handleJoin = (e) => {
        e.preventDefault();
        if (playerName.trim() && roomCode.trim()) {
            
            socket.emit("joinRoom", { room: roomCode, name: playerName,mode:mode });
            navigate('/game', { state: { playerName: playerName, roomId: roomCode, join:Boolean(true)} });


        }
    };



    const handleCreate = async  (e) => {
        e.preventDefault();
        if (playerName.trim()) {
            const response = await axios.post(CREATE_ROOM_URL, { name:playerName, create:true,mode:mode}, {headers:{"Content-Type":"application/json"}});
            const roomId = response.data.room;
            console.log(roomId, "roomId");

            socket.emit("joinRoom", { room: roomId, name: playerName,mode:mode });

            navigate('/game', { state: { playerName: playerName, roomId:roomId } });
        }
    };

    return (
        <div className="relative h-screen">
            {/* Arka plan videosu */}
            <video 
                autoPlay 
                loop  
                muted 
                src="codeFloating1.mp4" 
                className="absolute top-0 left-0 min-w-full min-h-full w-auto h-auto object-cover"
            > 
                <source src="intro.mp4" type="video/mp4" />
                Your browser does not support the video tag. 
            </video>   

            {/* Video üzerinde karartma katmanı */}
            <div className="absolute top-0 left-0 w-full h-full bg-black/60"></div>

            {/* Mevcut içerik */}
            <div className="relative z-10 flex flex-col items-center justify-center h-screen">
                <h1 className="text-4xl font-bold mb-6 text-green-400 animate-pulse">Welcome to the Rabbit Hole</h1>
                <div className="flex flex-col gap-8">
                    {/* Oyun Oluşturma Formu */}
                    <form onSubmit={handleCreate} className="flex flex-col gap-5">
                        <input
                            type="text"
                            value={playerName}
                            onChange={(e) => setPlayerName(e.target.value)}
                            placeholder="Enter your name"
                            maxLength="20"
                            required
                            className="px-4 py-2 text-lg bg-gray-800 border-2 border-green-500 rounded-lg w-64 
                            focus:outline-none focus:border-green-400 text-green-400 placeholder-green-600"
                        />
                        <button 
                            type="submit" 
                            disabled={!playerName.trim()}
                            className="px-6 py-2 text-lg text-gray-900 bg-green-500 rounded-lg 
                            transition-all duration-300 hover:bg-green-400 hover:shadow-lg hover:shadow-green-500/50 
                            disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed"
                        >
                            Create Game
                        </button>
                    </form>

                    {/* Oyuna Katılma Formu */}
                    <div className="flex flex-col items-center">
                        <div className="w-full border-t border-green-500/30"></div>
                        <span className="text-green-400 my-4">or</span>
                    </div>

                    <form onSubmit={handleJoin} className="flex flex-col gap-5">
                        <input
                            type="text"
                            value={roomCode}
                            onChange={(e) => setRoomCode(e.target.value)}
                            placeholder="Room Code"
                            maxLength="6"
                            required
                            className="px-4 py-2 text-lg bg-gray-800 border-2 border-green-500 rounded-lg w-64 
                            focus:outline-none focus:border-green-400 text-green-400 placeholder-green-600"
                        />
                        <button 
                            type="submit"
                            disabled={!playerName.trim() || !roomCode.trim()}
                            className="px-6 py-2 text-lg text-gray-900 bg-green-500 rounded-lg 
                            transition-all duration-300 hover:bg-green-400 hover:shadow-lg hover:shadow-green-500/50 
                            disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed"
                        >
                            Join Room
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default HomePage;


