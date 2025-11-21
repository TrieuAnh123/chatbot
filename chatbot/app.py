import streamlit as st
from chatbot.chatbot_logic_ai import generate_ai_response, create_order
import pandas as pd
import os

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Chatbot CSKH BHLĐ Triệu Gia",
    page_icon="💬",
    layout="wide",
)

# --- Tiêu đề ---
st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
    <h1>💬 Chatbot CSKH - BHLĐ Triệu Gia</h1>
    <p style='font-size:18px;'>🌸 Hỗ trợ tư vấn sản phẩm và tạo đơn hàng tự động cho khách hàng <b>Triệu Gia</b>.</p>
</div>
""", unsafe_allow_html=True)

# --- Bố cục chia 3 cột cân đối hơn ---
col1, col2, col3 = st.columns([1.1, 1.8, 1.1])

# ==============================
# CỘT 1 — DANH MỤC SẢN PHẨM
# ==============================
with col1:
    st.markdown("<h3 style='text-align:center;'>📦 Danh mục sản phẩm</h3>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("📂 Xem danh mục sản phẩm", use_container_width=True):
        product_path = os.path.join("data", "products.csv")

        if os.path.exists(product_path):
            try:
                df = pd.read_csv(product_path)
                st.session_state["products_data"] = df
                st.dataframe(df, use_container_width=True, height=430)
            except Exception as e:
                st.error(f"❌ Không thể đọc file sản phẩm: {e}")
        else:
            st.warning("⚠️ Không tìm thấy file `data/products.csv`.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 🔹 CỘT 2 — KHU VỰC TRÒ CHUYỆN
# ==============================
with col2:
    st.markdown("<h3 style='text-align:center;'>💬 Trò chuyện cùng trợ lý AI</h3>", unsafe_allow_html=True)

    # Lưu lịch sử hội thoại
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    chat_box_style = "border:1px solid #ccc; padding:12px; border-radius:10px; height:450px; overflow-y:auto; background:#fafafa;"

    st.markdown(f"<div style='{chat_box_style}'>", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.info("💡 Hãy bắt đầu trò chuyện bằng cách nhập câu hỏi bên dưới!")
    else:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"<p><b>👤 Quý khách:</b> {chat['content']}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p><b>🤖 Tôi:</b> {chat['content']}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Form nhập tin nhắn
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Nhập tin nhắn của bạn:")
    send = st.form_submit_button("📨 Gửi")

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    bot_reply = generate_ai_response(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    st.rerun()

# ==============================
# 🔹 CỘT 3 — FORM TẠO ĐƠN HÀNG
# ==============================
with col3:
    st.markdown("<h3 style='text-align:center;'>🧾 Tạo đơn hàng nhanh</h3>", unsafe_allow_html=True)

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
                st.success(f"✅ Đã tạo đơn hàng cho {customer_name}!")
