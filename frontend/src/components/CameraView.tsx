import React, { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import { identifyFace } from '../api/FaceApi';

interface CameraViewProps {
  onMatch: (student: any) => void; // Callback báo cho cha khi match
}

const videoConstraints = {
  width: 500,
  height: 300,
  facingMode: 'user',
};

export default function CameraView({ onMatch }: CameraViewProps) {
  const webcamRef = useRef<Webcam>(null);
  const isProcessing = useRef(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const detect = async () => {
      if (!webcamRef.current || isProcessing.current) return;

      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) {
        setError('Không thể lấy ảnh từ camera');
        return;
      }

      try {
        isProcessing.current = true;
        setIsLoading(true);
        setError(null);

        const student = await identifyFace(imageSrc);

        if (student) {
          onMatch(student); // Báo cho cha
        } else {
          setError('Không phát hiện khuôn mặt');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Lỗi không xác định');
      } finally {
        isProcessing.current = false;
        setIsLoading(false);
      }
    };

    const intervalId = setInterval(detect, 5000); // 5s gọi 1 lần
    return () => clearInterval(intervalId);
  }, [onMatch]);

  return (
    <div>
      <Webcam
        audio={false}
        height={300}
        width={500}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={videoConstraints}
      />
      {isLoading && <p>Đang xử lý...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}
