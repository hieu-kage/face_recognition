export async function identifyFace(imageBase64) {
  const res = await fetch('http://localhost:8000/image/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_base64: imageBase64 }) 
  });

  const data = await res.json(); // chỉ đọc một lần

  if (data.status === 'success') {
    console.log("✅ Kết quả trả về từ backend:", data);
    return data;
  } else {
    console.error("❌ API trả về lỗi:", data); // dùng luôn data
    return null;
  }
}
