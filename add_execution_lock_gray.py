import streamlit as st
import time

if 'processing' not in st.session_state:
    st.session_state.processing = False

def lock_ui():
    st.session_state.processing = True

# --- 1. 文件上传区 ---
uploaded_file = st.file_uploader(
    "監査対象のPDFを選択してください", 
    type="pdf", 
    disabled=st.session_state.processing
)

# --- 2. 准备区（只有上传后才显示） ---
if uploaded_file and not st.session_state.processing:
    st.success(f"ファイル '{uploaded_file.name}' を読み込みました。")
    # 使用按钮作为“启动门”，利用它的 on_click 触发变灰
    st.button("AI監査を実行する", on_click=lock_ui, type="primary")

# --- 3. 核心处理区 ---
if st.session_state.processing:
    # 此时，由于 lock_ui 已经运行，顶部的 file_uploader 会立即变灰
    progress_bar = st.progress(0)
    status = st.empty()
    
    try:
        status.text("ステップ 1: AIが解析中...")
        with st.spinner("思考中..."):
            time.sleep(3) # 模拟 Gemini 调用
        progress_bar.progress(100)
        st.success("監査完了！")
    finally:
        st.session_state.processing = False
        st.rerun()