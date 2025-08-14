import React from 'react';
import CameraView from './components/CameraView.tsx';
import StudentInfo from './components/StudentInfo.tsx';
import './App.css';

function App() {
  const [student, setStudent] = React.useState(null);

  const handleMatch = (matchedStudent) => {
    setStudent(matchedStudent);

    // Xóa sau 5 giây
    setTimeout(() => {
      setStudent(null);
    }, 5000);
  };

  return ( 
    <div className="app-container"> 
      <div className="left-panel"> 
        <CameraView onMatch={handleMatch} />
      </div>
      <div className="right-panel">
        {student && <StudentInfo student={student} />}
      </div>
    </div>
  );
}

export default App;
