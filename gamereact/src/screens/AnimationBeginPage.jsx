import { useNavigate } from 'react-router-dom';

function AnimationBeginPage() {
    const navigate = useNavigate();

    const handleClick = (mode) => {
        console.log(mode, "mode");
        navigate('/intro', { state: { mode } });
    };

    return (
        <div className="h-screen w-screen flex"> 
            {/* Video Container */}
            <div className="w-full h-full"> 
                <video
                    src="intro.mp4"
                    className="w-full h-full object-cover opacity-100" 
                    autoPlay
                    muted  
                    loop 
                    playsInline
                />
                
                {/* Kırmızı Hap - Sol Taraf */}
                <div 
                    onClick={() => handleClick('red')}
                    className="absolute left-[30%] bottom-[30%] w-[20%] h-[20%] 
                    hover:bg-red-500/30 transition-colors duration-300 cursor-pointer
                    flex items-center justify-center group"
                >
                    <span className="text-white text-3xl font-bold opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        Red Mode
                    </span>
                    {/* Bilgi Balonu - Kırmızı */}
                    <div className="absolute bottom-full mb-4 w-64 opacity-0 group-hover:opacity-100 
                        transition-opacity duration-300 bg-red-900/90 text-white p-4 rounded-lg
                        border border-red-500/50 shadow-lg shadow-red-500/20">
                        <h3 className="text-lg font-bold mb-2">Red Mode</h3>
                        <p className="text-sm">
                            Choose the red pill to dive deep into reality.
                            This mode will offer you a real challenge.
                        </p>
                        <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 
                            border-8 border-transparent border-t-red-900/90"></div>
                    </div>
                </div>

                {/* Mavi Hap - Sağ Taraf */}
                <div  
                    onClick={()=>handleClick('blue')}
                    className="absolute right-[30%] bottom-[30%] w-[20%] h-[20%]
                    hover:bg-blue-500/30 transition-colors duration-300 cursor-pointer
                    flex items-center justify-center group"
                >
                    <span className="text-white text-3xl font-bold opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        Blue Mode
                    </span>
                    {/* Bilgi Balonu - Mavi */}
                    <div className="absolute bottom-full mb-4 w-64 opacity-0 group-hover:opacity-100 
                        transition-opacity duration-300 bg-blue-900/90 text-white p-4 rounded-lg
                        border border-blue-500/50 shadow-lg shadow-blue-500/20">
                        <h3 className="text-lg font-bold mb-2">Blue Mode</h3>
                        <p className="text-sm">
                            Choose the blue pill for a peaceful experience.
                            This mode will offer you a comfortable gaming experience.
                        </p>
                        <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 
                            border-8 border-transparent border-t-blue-900/90"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnimationBeginPage;