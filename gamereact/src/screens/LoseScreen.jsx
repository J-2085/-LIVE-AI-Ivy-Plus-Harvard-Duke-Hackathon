function LoseScreen() {
    return (
        <div className="relative h-screen w-screen overflow-hidden bg-black">
            {/* Background video */}
            <video 
                autoPlay 
                loop 
                muted 
                src="kaybetme.mp4"
                className="absolute top-0 left-0 min-w-full min-h-full w-auto h-auto object-cover"
            >
            </video>

            {/* Light darkening over video */}
            <div className="absolute top-0 left-0 w-full h-full bg-black/50"></div>

            {/* Lose message and content */}
            <div className="relative z-10 flex flex-col items-center justify-center h-full text-center">
                <h1 className="text-6xl font-bold mb-8 text-red-500 animate-pulse">
                    FAILED!
                </h1>
                
                <div className="space-y-6 text-white">
                    <p className="text-2xl font-medium animate-fade-in">
                        Lost in the Rabbit Hole
                    </p>
                    
                    <div className="mt-12 space-y-4">
                        <button 
                            onClick={() => window.location.href = '/'}
                            className="px-8 py-3 bg-red-600 hover:bg-red-700 
                            text-white rounded-lg transition-colors duration-300
                            border border-red-500 hover:border-red-400
                            shadow-lg shadow-red-500/20"
                        >
                            Try Again
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoseScreen;
