export async function identifyFace(imageBase64) {
  const res = await fetch('http://localhost:8000/image/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_base64: imageBase64 }) // ✅ đúng key
  });

  if (!res.ok) {
    const errorText = await res.text();
    console.error("❌ API trả về lỗi:", errorText);
    return null;
  }

  const data = await res.json();
  console.log("✅ Kết quả trả về từ backend:", data);  // ✅ In ra toàn bộ response
  return data.first_person || null;
}
