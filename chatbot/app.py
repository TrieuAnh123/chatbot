import streamlit as st
from chatbot.chatbot_logic_ai import generate_ai_response, create_order
import pandas as pd
import os

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Chatbot CSKH BHLĐ Triệu Gia",
    page_icon="💬",
    layout="wide"
)

# --- CSS tùy chỉnh để cải thiện giao diện chat ---
st.markdown("""
<style>
    .main-chat-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        background-color: white;
        height: 400px;
        overflow-y: auto;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #fafafa;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        border: 1px solid #bbdefb;
    }
    .bot-message {
        background-color: #f5f5f5;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #e0e0e0;
    }
    .message-sender {
        font-weight: bold;
        font-size: 0.85em;
        margin-bottom: 3px;
        color: #555;
    }
    .empty-chat {
        text-align: center;
        color: #777;
        padding: 50px 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- Tiêu đề ---
st.title("💬 Chatbot CSKH - BHLĐ Triệu Gia")
st.markdown("🌸 Hỗ trợ tư vấn sản phẩm và tạo đơn hàng tự động cho khách hàng **Triệu Gia**.")

# --- Bố cục chia 3 cột ---
col1, col2, col3 = st.columns([1.2, 2, 1.2])

# --- Cột 1: Danh mục sản phẩm ---
with col1:
    st.subheader("📦 Danh mục sản phẩm")

    if st.button("📂 Xem danh mục sản phẩm"):
        product_path = os.path.join("data", "products.csv")

        if os.path.exists(product_path):
            try:
                df = pd.read_csv(product_path)
                st.session_state["products_data"] = df
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Không thể đọc file sản phẩm: {e}")
        else:
            st.warning("⚠️ Không tìm thấy file `data/products.csv`.")

# --- Cột 2: Khu vực trò chuyện ---
with col2:
    st.subheader("💬 Trò chuyện cùng trợ lý AI CSKH:")

    # Lưu lịch sử hội thoại
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Khung chat chính với border
    st.markdown('<div class="main-chat-container">', unsafe_allow_html=True)
    
    # Hiển thị nội dung chat trong khung
    if not st.session_state.chat_history:
        st.markdown('<div class="empty-chat">💡 Hãy bắt đầu trò chuyện bằng cách nhập câu hỏi bên dưới!</div>', unsafe_allow_html=True)
    else:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f'''
                <div class="user-message">
                    <div class="message-sender">👤 Quý khách</div>
                    {chat['content']}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="bot-message">
                    <div class="message-sender">🤖 Trợ lý AI</div>
                    {chat['content']}
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Form nhập tin nhắn  ---
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Nhập tin nhắn của bạn:")
        send = st.form_submit_button("📨 Gửi")

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        bot_reply = generate_ai_response(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

        st.rerun()

# --- Cột 3: Form tạo đơn hàng ---
with col3:
    st.subheader("🧾 Tạo đơn hàng nhanh (tùy chọn)")

    with st.form("order_form"):
        customer_name = st.text_input("Tên khách hàng")
        address = st.text_input("Địa chỉ giao hàng")
        phone = st.text_input("Số điện thoại")
        product_name = st.text_input("Tên sản phẩm")
        quantity = st.number_input("Số lượng", min_value=1, step=1)

        submit = st.form_submit_button("Tạo đơn hàng")

        if submit:
            if not all([customer_name, address, phone, product_name]):
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin trước khi tạo đơn hàng.")
            else:
                create_order(customer_name, address, phone, product_name, quantity)
                st.success(f"✅ Đã tạo đơn hàng cho {customer_name} ({product_name} x {quantity}).")
