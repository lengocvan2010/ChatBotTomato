import streamlit as st
import requests

# URL của API FastAPI
API_URL = "http://127.0.0.1:8000/predict/"

st.title("Ứng dụng hỗ trợ chăm sóc cây cà chua")
st.write("Nhập mô tả hoặc tải lên hình ảnh cây cà chua để nhận tư vấn.")

# Form nhập liệu
with st.form("upload_form"):
    # Nhập mô tả
    text_input = st.text_input("Nhập mô tả về tình trạng cây (ví dụ: lá bị vàng, đốm đen, v.v.)", "")

    # Upload file
    uploaded_file = st.file_uploader("Tải lên hình ảnh cây cà chua (tùy chọn)", type=["jpg", "png", "jpeg"])

    # Nút gửi
    submit_button = st.form_submit_button("Dự đoán")

if submit_button:
    if not text_input:
        st.error("Vui lòng nhập mô tả tình trạng cây.")
    else:
        try:
            # Tạo payload cho request
            data = {"text": text_input}
            files = None  # Mặc định không có file

            # Nếu có file, thêm vào payload
            if uploaded_file:
                file_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, file_bytes, uploaded_file.type)}

            st.write("Tôi: " + text_input)

            # Gửi request tới API
            response = requests.post(API_URL, data=data, files=files)

            # Xử lý kết quả trả về
            if response.status_code == 200:
                result = response.json()  # Kết quả là dictionary
                # Lấy giá trị cụ thể từ result
                if "result" in result:
                    st.text("Kết quả: " + result["result"])  # Hiển thị giá trị từ key "result"
                else:
                    st.error("API trả về kết quả không mong đợi.")
            else:
                st.error(f"Lỗi từ API: {response.status_code} - {response.json().get('detail', 'Không rõ lỗi')}")


        except Exception as e:
            st.error(f"Lỗi khi kết nối đến API: {str(e)}")
