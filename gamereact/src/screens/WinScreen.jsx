function WinScreen() {
    return (
        <div className="relative h-screen w-screen overflow-hidden bg-black">
            {/* Background video */}
            <video 
                autoPlay 
                loop 
                muted 
                src="kazanma.mp4"  
                className="absolute top-0 left-0 min-w-full min-h-full w-auto h-auto object-cover"
            >
            </video>

            {/* Light darkening over video */}
            <div className="absolute top-0 left-0 w-full h-full bg-black/40"></div>

            {/* Victory message and content */}
            <div className="relative z-10 flex flex-col items-center justify-center h-full text-center">
                <h1 className="text-6xl font-bold mb-8 text-green-400 animate-pulse">
                    CONGRATULATIONS!
                </h1>
                
                <div className="space-y-6 text-white">
                    <p className="text-2xl font-medium animate-fade-in">
                        Successfully Escaped the Rabbit Hole
                    </p>
                    
                    <div className="mt-12">
                        <button 
                            onClick={() => window.location.href = '/'}
                            className="px-8 py-3 bg-green-500 hover:bg-green-600 
                            text-white rounded-lg transition-colors duration-300
                            border border-green-400 hover:border-green-300
                            shadow-lg shadow-green-500/20"
                        >
                            Return to Home
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WinScreen;
