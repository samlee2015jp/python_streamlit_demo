import streamlit as st
import time
import random

# --- 1. 初始化 Session State ---
if 'processing' not in st.session_state:
    st.session_state.processing = False

# 回调函数：点击按钮时第一时间锁住 UI
def lock_ui():
    st.session_state.processing = True

# --- 2. 页面布局与输入区 ---
st.set_page_config(page_title="金融監査システム", layout="centered")
st.title("⚖️ 金融合規監査集成系统")

# 模拟必需的选项（例如：选择审计级别）
audit_type = st.radio(
    "監査タイプを選択してください（必需）",
    options=["未選択", "基本監査", "詳細解析"],
    index=0,
    disabled=st.session_state.processing
)

# 文件上传（必需）
uploaded_file = st.file_uploader(
    "監査対象のPDFをアップロードしてください", 
    type="pdf",
    disabled=st.session_state.processing
)

# --- 3. 触发与校验逻辑 ---
# 使用 on_click=lock_ui 确保点击瞬间页面组件全部灰掉
if st.button("監査プロセスを開始", on_click=lock_ui, disabled=st.session_state.processing, type="primary"):
    
    # --- 【关键点】校验逻辑 ---
    # 如果不符合预设条件，我们需要“解锁”并退出
    error_msg = None
    if audit_type == "未選択":
        error_msg = "監査タイプを選択してください。"
    elif uploaded_file is None:
        error_msg = "ファイルをアップロードしてください。"

    if error_msg:
        st.error(f"⚠️ 入力エラー: {error_msg}")
        # 重置状态并停止，让用户重新选择
        st.session_state.processing = False
        # 这里不需要 st.rerun，因为我们想让错误信息显示在当前页面
        # 后续代码由于 processing 为 False 不会执行
    else:
        # --- 4. 核心处理区（里程碑模式） ---
        st.info("🔄 処理を開始します。そのままお待ちください...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 里程碑 1
            status_text.text("ステップ 1/3: データを読み込んでいます...")
            progress_bar.progress(20)
            time.sleep(1) # 模拟处理

            # 里程碑 2：最耗时的 LLM 访问
            status_text.text("ステップ 2/3: Gemini AI が解析中（これには時間がかかります）...")
            with st.spinner("AIが思考中..."):
                # 模拟进度波动
                for p in range(21, 81, 5):
                    time.sleep(random.uniform(0.2, 0.5))
                    progress_bar.progress(p)
            
            # 里程碑 3
            status_text.text("ステップ 3/3: 最終レポートを作成中...")
            progress_bar.progress(100)
            
            st.success("✅ 監査が完了しました！")
            st.balloons() # 庆祝动画
            
            # 这里可以放置下载按钮等
            st.download_button("レポートをダウンロード", data="Audit Report Contents", file_name="report.txt")

        except Exception as e:
            st.error(f"❌ 予期せぬエラーが発生しました: {e}")
        
        finally:
            # 处理结束，释放全局锁
            st.session_state.processing = False
            # 按钮恢复可用状态
            if not error_msg:
                st.button("別のファイルを処理する")

else:
    # 初始状态下的提示
    if not st.session_state.processing:
        st.write("📢 上記の項目を入力し、ボタンを押してください。")