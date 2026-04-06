import streamlit as st
import time
import random

# 1. 初始化 Session State 状态锁
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_task():
    # 触发开始任务
    st.session_state.processing = True

# --- 界面布局 ---
st.title("🚀 金融数据集成处理系统")
st.write("演示：多重执行防止 + 动态百分比 + 组件禁用")

# 2. 操作禁止：当 processing 为 True 时，禁用按钮和输入框
user_input = st.text_input(
    "请输入 CSV 路径", 
    placeholder="data_25cols.csv", 
    disabled=st.session_state.processing
)

# 使用 on_click 触发状态变更
start_btn = st.button(
    "开始执行行拼接", 
    on_click=start_task, 
    disabled=st.session_state.processing
)

# 3. 核心处理逻辑
if st.session_state.processing:
    st.info("🔄 正在处理数据，请勿重复点击...")
    
    # 创建动态显示区域
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 模拟任务执行
    try:
        total_steps = 10
        for i in range(total_steps):
            # 模拟变动百分比
            percent = (i + 1) * 10
            status_text.text(f"当前进度: {percent}% - 正在处理第 {i+1} 块数据...")
            progress_bar.progress(percent)
            
            # 模拟随机耗时（波动性）
            time.sleep(random.uniform(0.3, 0.8)) 
        
        st.success("✅ CSV 拼接完成！NaN 已填充为空字符。")
    
    except Exception as e:
        st.error(f"❌ 处理出错: {e}")
    
    finally:
        # 重要：无论成功失败，最后都要释放状态锁
        st.session_state.processing = False
        # 强制刷新页面以解除组件禁用状态
        st.rerun()

else:
    st.write("📢 系统就绪，等待操作。")