import React from "react";

 function StudentInfo({ student }) {
    if (!student) return <p>Chưa nhận diện được khuôn mặt</p>;
  
    return (
      <>
        <h3>Thông tin sinh viên</h3>
        <img src={student.avatarUrl} alt="avatar" width={150} />
        <p><strong>Họ tên:</strong> {student.name}</p>
        <p><strong>Mã SV:</strong> {student.id}</p>
        <p><strong>Lớp:</strong> {student.class}</p>
        <p><strong>Trạng thái:</strong> {student.status}</p>
      </>
    );
  }
export default StudentInfo;