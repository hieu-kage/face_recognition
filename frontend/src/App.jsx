import React from 'react';
import CameraView from './components/CameraView.tsx';
import StudentInfo from './components/StudentInfo.tsx';
import './App.css';

function App() {
  const [student, setStudent] = React.useState(null);

  return (
    <div className="app-container">
      <div className="left-panel">
        <CameraView onMatch={setStudent} />
      </div>
      <div className="right-panel">
        <StudentInfo student={student} />
      </div>
    </div>
  );
}

export default App;
