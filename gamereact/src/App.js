import './App.css';
import HomePage from './screens/HomePage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import GamePage from './screens/GamePage';
import AnimationBeginPage from './screens/AnimationBeginPage';
import WinScreen from './screens/WinScreen';
import LoseScreen from './screens/LoseScreen';


function App() {
  return (
    <BrowserRouter>
      <Routes initialIndex={0}>
      <Route path="/"  element={<AnimationBeginPage />} />
        <Route path="/intro" element={<HomePage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/win" element={<WinScreen />} />
        <Route path="/lose" element={<LoseScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
