import streamlit as st
import time
import random

# 1. セッション状態（Session State）の初期化：二重実行防止用フラグ
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_task():
    # 処理開始フラグを立てる
    st.session_state.processing = True

# --- 画面レイアウト ---
st.title("🚀 金融データ統合処理システム")
st.write("デモ：二重実行防止 ＋ 動的進捗表示 ＋ 操作無効化機能")

# 2. 操作制限：処理中（processing == True）はアップローダーとボタンを無効化
file_master = st.file_uploader(
    "ベースとなるPDFファイルを選択してください (基準25列データ)", 
    type="pdf", 
    disabled=st.session_state.processing
)

# on_clickを使用して状態変更をトリガー
start_btn = st.button(
    "データ統合処理を開始", 
    on_click=start_task, 
    disabled=st.session_state.processing
)

# 3. メイン処理ロジック
if st.session_state.processing:
    st.info("🔄 データを処理中です。画面を閉じたり、再操作しないでください...")
    
    # 動的表示エリアの作成
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # タスク実行のシミュレーション
    try:
        total_steps = 10
        for i in range(total_steps):
            # 進捗率のシミュレーション
            percent = (i + 1) * 10
            status_text.text(f"現在の進捗: {percent}% - 第 {i+1} ブロックを処理中...")
            progress_bar.progress(percent)
            
            # ランダムな待機時間（処理のゆらぎをシミュレート）
            time.sleep(random.uniform(0.3, 0.8)) 
        
        st.success("✅ データ統合が完了しました！欠損値（NaN）は空文字に置換済みです。")
    
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
    
    finally:
        # 重要：成功・失敗に関わらず、最後に処理フラグを解除
        st.session_state.processing = False
        # 画面をリロードしてボタン等の無効化を解除
        st.rerun()

else:
    st.write("📢 システム待機中。操作を開始してください。")