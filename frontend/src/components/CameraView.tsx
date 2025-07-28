import React, { useRef, useCallback, useState } from 'react';
import Webcam from 'react-webcam';
import { identifyFace } from '../api/FaceApi';

interface CameraViewProps {
  onMatch: (student: any) => void; // Replace 'any' with your student type
}
interface Student {
  id: string;
  name: string;
  studentId: string;
  class?: string;
  // Add other student properties as needed
}
const videoConstraints = {
  width: 500,
  height: 300,
  facingMode: "user"
};

export default function CameraView({ onMatch }: CameraViewProps) {
  const webcamRef = useRef<Webcam>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matchedStudent, setMatchedStudent] = useState<Student | null>(null);

  const capture = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      setMatchedStudent(null);
      
      const imageSrc = webcamRef.current?.getScreenshot();
      if (!imageSrc) {
        throw new Error('Failed to capture image');
      }

      const student = await identifyFace(imageSrc);
      if (student) {
        setMatchedStudent(student);
        onMatch(student);
      } else {
        setError('No face detected');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
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
        videoConstraints={videoConstraints}
      />
      <button onClick={capture} disabled={isLoading}>
        {isLoading ? 'Đang xử lý...' : 'Điểm danh'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {matchedStudent && (
        <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
          <h4>Thông tin sinh viên:</h4>
          <p><strong>Họ tên:</strong> {matchedStudent.name}</p>
          <p><strong>MSSV:</strong> {matchedStudent.studentId}</p>
          {matchedStudent.class && (
            <p><strong>Lớp:</strong> {matchedStudent.class}</p>
          )}
        </div>
      )}
    </div>
  );
}