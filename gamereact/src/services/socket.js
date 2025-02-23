import { io } from "socket.io-client";

// Socket bağlantısını oluştur
const socket = io("https://game-backend-759420319197.us-central1.run.app", { transports: ["websocket"] });

// Bağlantı durumunu kontrol et
socket.on("connect", () => {
    console.log("Socket.IO bağlantısı başarılı");
});

socket.on("disconnect", () => {
    console.log("Socket.IO bağlantısı kesildi");
});

export default socket; 