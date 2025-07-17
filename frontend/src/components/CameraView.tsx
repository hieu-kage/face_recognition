  import React, { useRef, useCallback } from 'react';
  import Webcam from 'react-webcam';
  import { identifyFace } from '../api/FaceApi';

  const videoConstraints = {
    width: 500,
    height: 300,
    facingMode: "user"
  };

  export default function CameraView({ onMatch }) {
    const webcamRef = useRef(null);

    const capture = useCallback(async () => {
      const imageSrc = webcamRef.current.getScreenshot();
      console.log("Ảnh base64 (100 ký tự đầu):", imageSrc.slice(0, 100)); 
      const student = await identifyFace(imageSrc); 
      if (student) onMatch(student);
    }, [webcamRef, onMatch]);

    return (
      <div className="camera-box" style={{ display: 'flex', flexDirection: 'column', alignContent: 'center' }}> 
        <h3>Camera điểm danh</h3>
        <Webcam
          audio={false}
          height={300}
          width={500}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
        />
        <button onClick={capture}>Điểm danh</button>
      </div>
    );
  }
