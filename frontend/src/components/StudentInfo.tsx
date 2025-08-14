import React from 'react';

interface User {
  name: string;
  student_id: string;
  email?: string;
}

interface StudentData {
  status: string;
  user: User;
  input_image_base64?: string;
  matching_image_base64?: string;
}

interface StudentInfoProps {
  student: StudentData | null;
}

export default function StudentInfo({ student }: StudentInfoProps) {
  if (!student || !student.user) return null;

  const { name, student_id, email} = student.user;

  return (
    <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
      <h4>Thông tin sinh viên:</h4>
      <p><strong>Họ tên:</strong> {name}</p>
      <p><strong>MSSV:</strong> {student_id}</p>

      {/* Hiển thị ảnh */}
      <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
        {student.input_image_base64 && (
          <div>
            <p><strong>Ảnh nhận diện:</strong></p>
            <img
              src={`data:image/jpeg;base64,${student.input_image_base64}`}
              alt="Input"
              style={{ maxWidth: '200px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
        )}

        {student.matching_image_base64 && (
          <div>
            <p><strong>Ảnh gốc khớp:</strong></p>
            <img
              src={`data:image/jpeg;base64,${student.matching_image_base64}`}
              alt="Matching"
              style={{ maxWidth: '200px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
