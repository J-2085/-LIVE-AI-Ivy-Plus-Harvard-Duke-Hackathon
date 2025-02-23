import { useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import socket from '../services/socket';
import { useNavigate } from 'react-router-dom';

function GamePage() {
    const navigate = useNavigate();

    const location = useLocation();
    const playerName = location.state?.playerName || "Misafir";
    const roomId = location.state?.roomId || "test";
    const [chatMessages, setChatMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [currentSpeaker, setCurrentSpeaker] = useState(1);
    const [timer, setTimer] = useState(15);
    const [isVotingTime, setIsVotingTime] = useState(false);
    const [gamePhase, setGamePhase] = useState('speaking');
    const [activePlayers, setActivePlayers] = useState([]);
    const [selectedVote, setSelectedVote] = useState(null);
    const [winner, setWinner] = useState(null);
    const [userGameID,setUserGameID] = useState(0);

    socket.on("newMessage", (msg) => {
        console.log("newMessage");
        setChatMessages((prev) => [...prev, msg]);
    });

    useEffect(() => {
        socket.on("game_ended", (data) => {
            console.log("game_ended", data);
            setWinner(data.winner);
            
            game_end(data.winner);
        });

        return () => {
            socket.off("game_ended");
        };
    }, []);

    const game_end = (winnerTeam) => {
        console.log("Game End Called with winner:", winnerTeam);
        if(winnerTeam === "Humans"){
            console.log("Humans win");
            navigate('/win');
        } else {
            console.log("AIs win");
            navigate('/lose');
        }
    };

    socket.on("update_game", (data) => {
        console.log("Data",data);
        const { speaker, time_left, phase, active_players,player_list } = data;
        setCurrentSpeaker(speaker);
        setTimer(time_left);
        setGamePhase(phase);
        setActivePlayers(active_players || []);
        setIsVotingTime(phase === 'voting');
        setUserGameID(player_list?.find(player => player.player_name === playerName)?.player_id);
        console.log("User Game ID",player_list?.find(player => player.player_name === playerName)?.player_id);
    });

    socket.on("recMessage", (data) => {
        console.log("MEsajlar çıktı");
        console.log(data, "content");
        setChatMessages((prev) => {
            if (prev.some(msg => msg.text === data?.content?.message)) {
                return prev;
            }
            return [...prev, { sender: data?.content?.name || "Misafir", text: data?.content?.message || "Mesaj gelmemiş"}];
        });
        console.log("Received: ", data);
    });

    socket.on("message", (data) => {
        console.log("MEsajlar çıktı");
        console.log(data, "content");
        setChatMessages((prev) => {
            if (prev.some(msg => msg.text === data?.content?.message)) {
                return prev;
            }
            return [...prev, { sender: data?.content?.name || "Misafir", text: data?.content?.message || "Mesaj gelmemiş"}];
        });
        console.log("Received: ", data);
    });

    const handleSendMessage = (e) => {
        e.preventDefault();
        if (newMessage.trim()) {
            socket.emit("newMessage", { data: newMessage, room:roomId, name:`Karakter ${userGameID}`});
            console.log(newMessage, "handleSendMessage");
            setChatMessages([...chatMessages, { sender: "You", text: newMessage }]);
            setNewMessage('');
        }
    };

    return (
        <div className="flex h-screen bg-gray-900">
            {/* Oyun Alanı - %70 */}
            <div className="w-[70%] h-screen p-4 border-r border-green-500/30 overflow-hidden">
                {/* Timer ve Konuşmacı Bilgisi */}
                <div className="mb-6 text-center bg-gray-800/50 p-4 rounded-lg border border-green-500/30">
                    {winner && (
                        <div className="text-2xl text-yellow-400 bg-gray-800 p-4 mb-4 rounded-lg border border-yellow-500/50">
                            Game Over! Winner: {winner} 
                        </div>
                    )}
                    {gamePhase === 'waiting' ? (
                        <div className="text-2xl text-blue-400 bg-gray-800 p-4 rounded-lg border border-blue-500/50">
                            <div className="flex items-center justify-center gap-3">
                                <div className="animate-spin w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full"></div>
                                <span>Waiting for Players...</span>
                            </div>
                            <div className="text-sm text-blue-300 mt-2">
                                Waiting for other players to join to start the game
                            </div>
                        </div>
                    ) : gamePhase === 'voting' ? (
                        <div className="text-2xl text-green-400 bg-gray-800 p-4 rounded-lg border border-green-500/50 animate-pulse">
                            Voting Time!
                        </div>
                    ) : (
                        <div className="space-y-2">
                            <div className="text-xl text-green-400">
                                Speaking Turn: Character {currentSpeaker}
                            </div>
                            <div className="text-3xl font-bold text-green-500">
                                Time Left: {timer} seconds
                            </div>
                        </div>
                    )}
                </div>

                {/* Karakterler Grid */}
                <div className="grid grid-cols-4 grid-rows-2 gap-6 h-[calc(100%-8rem)]">
                    {[...Array(8)].map((_, index) => (
                        <div 
                            key={index}
                            onClick={() => {
                                if (gamePhase === 'voting') {
                                    setSelectedVote(index + 1);
                                    socket.emit("submit_vote", {
                                        room: roomId,
                                        voter: userGameID,
                                        voted_for: index + 1
                                    }); 
                                }
                            }}
                            className={`
                                relative p-4 rounded-lg
                                flex items-center justify-center
                                transition-all duration-300 cursor-pointer
                                ${userGameID === index + 1 ? 'ring-2 ring-yellow-400 ring-offset-2 ring-offset-gray-900' : ''}
                                ${currentSpeaker === index + 1 ? 'bg-green-500/20 border-2 border-green-400 shadow-lg shadow-green-400/20 scale-105 z-10' 
                                  : gamePhase === 'voting' && selectedVote === index + 1 ? 'bg-purple-500/20 border-2 border-purple-400 shadow-lg shadow-purple-400/20 scale-105 z-10'
                                  : !activePlayers.includes(index + 1) ? 'bg-gray-800/50 border border-red-500/30 opacity-50' 
                                  : 'bg-gray-800 border border-green-500/30 hover:border-green-500/50'}
                            `}
                        >
                            <div className="text-center">
                                <div className={`text-lg font-semibold mb-2 
                                    ${userGameID === index + 1 ? 'text-yellow-400' : ''}
                                    ${currentSpeaker === index + 1 ? 'text-green-400' 
                                    : gamePhase === 'voting' && selectedVote === index + 1 ? 'text-purple-400'
                                    : !activePlayers.includes(index + 1) ? 'text-red-400/70'
                                    : 'text-green-500/70'}`}>
                                    Character {index + 1} {userGameID === index + 1 && '(You)'}
                                </div>
                                {currentSpeaker === index + 1 && gamePhase === 'speaking' && (
                                    <div className="text-sm text-green-400/80 bg-green-500/10 px-3 py-1 rounded-full">
                                        Speaking...
                                    </div>
                                )}
                                {!activePlayers.includes(index + 1) && (
                                    <div className="text-sm text-red-400/80 bg-red-500/10 px-3 py-1 rounded-full">
                                        Inactive
                                    </div>
                                )}
                                {gamePhase === 'voting' && selectedVote === index + 1 && (
                                    <div className="text-sm text-purple-400/80 bg-purple-500/10 px-3 py-1 rounded-full">
                                        Selected
                                    </div>
                                )}
                            </div>
                            {userGameID === index + 1 && (
                                <div className="absolute -top-3 -right-3 bg-yellow-400 text-xs text-gray-900 px-2 py-1 rounded-full font-semibold">
                                    Your Card
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Chat Alanı - %30 */}
            <div className="w-[30%] h-screen p-4 flex flex-col overflow-hidden">
                <div className="flex flex-col gap-2 mb-4">
                    <div className="text-green-400 text-xl font-semibold">
                        Chat - {playerName}
                    </div>
                    <div className="text-green-500/70 text-sm flex items-center gap-2">
                        <span>Oda Kodu:</span>
                        <span className="bg-gray-800 px-3 py-1 rounded-md border border-green-500/30 font-mono">
                            {roomId}
                        </span>
                    </div>
                </div>
                
                {/* Mesajlar */}
                <div className="flex-1 bg-gray-800 rounded-lg p-4 mb-4 overflow-y-auto
                    border border-green-500/30">
                    {chatMessages.map((msg, index) => (
                        <div key={index} className="mb-2">
                            <span className="text-green-500 font-semibold">{msg.sender}: </span>
                            <span className="text-green-400">{msg.text}</span> 
                        </div>
                    ))}
                </div>

                {/* Mesaj Gönderme Formu */}
                <form onSubmit={handleSendMessage} className="flex gap-2">
                    <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder={
                            gamePhase === 'voting' 
                                ? "You can't talk during voting!" 
                                : currentSpeaker !== userGameID 
                                    ? "It's not your turn to speak, you need to wait..." 
                                    : "Type your message..."
                        }
                        disabled={gamePhase === 'voting' || currentSpeaker !== userGameID}
                        className="flex-1 px-4 py-2 bg-gray-800 border border-green-500/50 rounded-lg
                        text-green-400 placeholder-green-600/50 focus:outline-none focus:border-green-400
                        disabled:bg-gray-700 disabled:border-gray-600 disabled:cursor-not-allowed"
                    />
                    <button
                        type="submit"
                        className="px-4 py-2 bg-green-500 text-gray-900 rounded-lg
                        hover:bg-green-400 transition-colors duration-300
                        disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed"
                        disabled={!newMessage.trim() || gamePhase === 'voting' || currentSpeaker !== userGameID}
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}

export default GamePage;
