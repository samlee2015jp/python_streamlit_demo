import streamlit as st
import time
from io import BytesIO

# --- 1. 状态初始化 ---
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = []
if 'pdf_result' not in st.session_state:
    st.session_state.pdf_result = None  # 用于存储生成的 PDF 字节流

# --- 2. 校验回调函数 ---
def validate_and_start():
    errors = []
    if not st.session_state.get('audit_type'):
        errors.append("「監査タイプ」を選択してください。")
    if not st.session_state.get('priority_level'):
        errors.append("「優先順位」を選択してください。")
        
    if errors:
        st.session_state.error_msg = errors
        st.session_state.processing = False
    else:
        st.session_state.error_msg = []
        st.session_state.processing = True
        st.session_state.pdf_result = None # 开始新任务，清空旧结果

# --- 3. 界面布局 ---
st.title("⚖️ 金融合规审计系统 (带下载功能)")

# 显示错误
if st.session_state.error_msg:
    for msg in st.session_state.error_msg:
        st.error(msg)

# 输入区域
col1, col2 = st.columns(2)
with col1:
    st.radio("監査タイプ:", ["広告審査", "契約書確認"], index=None, key="audit_type", disabled=st.session_state.processing)
with col2:
    st.radio("優先順位:", ["高", "低"], index=None, key="priority_level", disabled=st.session_state.processing)

# 执行按钮
st.button("审计开始", on_click=validate_and_start, disabled=st.session_state.processing, type="primary")

# --- 4. 核心处理逻辑 ---
if st.session_state.processing:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("AI审计中...")
        for i in range(1, 101):
            time.sleep(0.02)
            progress_bar.progress(i)
        
        # 模拟生成 PDF 字节流
        # 在实际代码中，这里是你的 PDF 生成函数返回的 bytes
        fake_pdf = BytesIO()
        fake_pdf.write(b"This is a dummy audited PDF content.")
        st.session_state.pdf_result = fake_pdf.getvalue()
        
        st.success("✅ 审计完成！报告已准备好下载。")
        
    finally:
        st.session_state.processing = False
        # 💡 这里不执行 rerun，为了让成功信息和下载按钮保持显示
        # 但 UI 已经通过状态恢复，可以再次选择了

# --- 5. 结果显示与下载区域 ---
if st.session_state.pdf_result and not st.session_state.processing:
    st.divider()
    st.markdown("### 📄 审计报告下载")
    
    col_dl, col_reset = st.columns([1, 1])
    
    with col_dl:
        st.download_button(
            label="📥 下载 PDF 报告",
            data=st.session_state.pdf_result,
            file_name="audit_report.pdf",
            mime="application/pdf"
        )
    
    with col_reset:
        if st.button("清除结果并重新开始"):
            st.session_state.pdf_result = None
            st.rerun()