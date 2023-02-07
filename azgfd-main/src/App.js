import logo from './logo.svg';
import img2 from'./img2.png';
import './App.css';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={img2} className="App-logo" alt="logo" />
        <p className="greeting">
          Welcome! 
          <span>Please choose one of the below options.</span>
        </p>
        <ul class="selections">
          <a
            className="nav-link"
            href="https://docs.google.com/spreadsheets/d/1_RyT4Af2-h3I4QhH54W8xKC2mMbebXPHp1qDH9N4BL8/edit?usp=sharing"
            target="_blank"
            rel="noopener noreferrer"
          >
            Excel Data
          </a>
          <a
            className="nav-link"
            href="https://docs.google.com/document/d/1B01L0DdIiTkL5GGSegKxEHFT2ej8w_uey8H95bxRleA/edit?usp=sharing"
            target="_blank"
            rel="noopener noreferrer"
          >
            User Manual
          </a>
        </ul>
      </header>
    </div>
  );
}

export default App;
