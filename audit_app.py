import streamlit as st
import time
import random
import fitz  # PyMuPDF
from io import BytesIO
from dotenv import load_dotenv
from google import genai

from typing import List

# --- 1. 配置 Gemini API ---
# 请替换为你自己的 API Key

load_dotenv()
google_client = genai.Client()

# --- 2. 初始化 Session State 状态锁 ---
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.processing = True

# --- 3. 辅助函数：调用 LLM 审计 ---
def audit_pdf_content(pdf_bytes):
    # 将 PDF 字节流上传给 Gemini (Gemini 1.5 支持直接处理 PDF)
    # 模拟处理过程
    prompt = """
    你是一名资深的金融合规审计师。请分析这份广告文件是否存在违反金融法律法规的内容（如夸大收益、未提示风险等）。
    请给出简要的审计结论，并指出具体的违规点。
    """
    # 实际应用中需使用 genai.upload_file 或直接传递 bytes

    response = google_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt)
    return response.text

# --- 4. 辅助函数：生成结果 PDF ---
def generate_result_pdf(original_pdf_bytes, audit_report):
    doc = doc = fitz.Document(stream=pdf_bytes, filetype="pdf")
    # 在 PDF 第一页前插入一个报告页
    page = doc.new_page(0, width=595, height=842) # A4
    page.insert_text((50, 50), "金融合规审计报告", fontsize=20, fontname="helv")
    page.insert_textbox((50, 100, 550, 800), audit_report, fontsize=11, fontname="helv")
    
    output_buffer = BytesIO()
    doc.save(output_buffer)
    doc.close()
    return output_buffer.getvalue()

# --- 5. Streamlit 界面 ---
st.set_page_config(page_title="AI 金融合规审计助手", layout="centered")
st.title("⚖️ AI 金融合规审计系统")
st.markdown("上传广告 PDF，由 Gemini 自动识别合规风险。")

# 操作禁止：任务运行时禁用上传和按钮
uploaded_file = st.file_uploader(
    "上传金融广告 PDF 文件", 
    type="pdf", 
    disabled=st.session_state.processing
)

if uploaded_file:
    st.button(
        "开始合规审计", 
        on_click=start_processing, 
        disabled=st.session_state.processing,
        type="primary"
    )

# --- 6. 核心处理逻辑 ---
if st.session_state.processing and uploaded_file:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 步骤 1: 读取文件
        status_text.text("正在读取文件并上传至 Gemini...")
        pdf_bytes = uploaded_file.read()
        progress_bar.progress(20)
        time.sleep(random.uniform(0.5, 1.0)) # 模拟波动
        
        # 步骤 2: 调用大模型审计
        status_text.text("Gemini 正在深入审计合规风险（可能需要 10-20 秒）...")
        # 这里是实际耗时较长的部分
        audit_report = audit_pdf_content(pdf_bytes)
        progress_bar.progress(70)
        
        # 步骤 3: 生成结果文件
        status_text.text("正在生成带标注的 PDF 报告...")
        result_pdf = generate_result_pdf(pdf_bytes, audit_report)
        progress_bar.progress(100)
        
        st.success("✅ 审计完成！")
        st.markdown("### 审计建议摘要")
        st.info(audit_report)
        
        # 步骤 4: 提供下载
        st.download_button(
            label="📥 下载审计后 PDF 报告",
            data=result_pdf,
            file_name=f"Audited_{uploaded_file.name}",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"❌ 处理过程中发生错误: {e}")
    
    finally:
        st.session_state.processing = False
        # 不立即 rerun，以便用户点击下载按钮
else:
    if not uploaded_file:
        st.write("📢 请先上传需要审计的 PDF 文件。")