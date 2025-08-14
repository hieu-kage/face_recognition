import React from 'react';

interface User {
  name: string;
  studentId: string;
  class?: string;
}

interface StudentInfoProps {
  student: { status: string; user: User } | null;
}

export default function StudentInfo({ student }: StudentInfoProps) {
  if (!student || !student.user) return null;

  const { name, studentId, class: className } = student.user;

  return (
    <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
      <h4>Thông tin sinh viên:</h4>
      <p><strong>Họ tên:</strong> {name}</p>
      <p><strong>MSSV:</strong> {studentId}</p>
      {className && <p><strong>Lớp:</strong> {className}</p>}
    </div>
  );
}
