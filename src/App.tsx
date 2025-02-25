import "./App.css";
import { useState } from "react";
import TextPanel from "./components/TextPanel";
import Canvas from "./components/Canvas";
import Authors from "./components/Authors";
import Info from "./components/Info";

function App() {
  const [isTextPanelOpen, setIsTextPanelOpen] = useState(true);

  const handleTogglePanel = () => {
    setIsTextPanelOpen(!isTextPanelOpen);
  };

  return (
    <>
      <div>
        <div className="relative w-full h-full overflow-hidden">
          <Info />
          <TextPanel isOpen={isTextPanelOpen} onToggle={handleTogglePanel} />
          <Canvas isTextPanelOpen={isTextPanelOpen} />
          <Authors />
        </div>
      </div>
    </>
  );
}

export default App;
