import os
import streamlit as st

# 匯入 6 歲男童個案病歷資料
from patient_case import CASE_DATA

# ─── STREAMLIT 網頁基礎設定 ───
st.set_page_config(page_title="小兒臨床決策模擬", layout="wide")
st.title("🩺 臨床情境模擬：你與急診護理師互動視窗")

# ─── 🔊 音效播放組件 (GitHub 正確版) ───

def play_background_ambient():
    """【聲道 1】在網頁背景持續『循環』播放急診室繁忙的吵雜聲 (Ambient)"""
    audio_path = "sounds/er_room.mp3" 
    
    if os.path.exists(audio_path):
        # loop=True 讓背景音無限循環
        st.audio(audio_path, format="sounds/er_room.mp3", loop=True, autoplay=True)

def play_crisis_sounds():
    """【聲道 2】同時疊加播放『男童哭聲』與『媽媽罵人聲』，兩者會一起蓋在背景音上面"""
    cry_path = "sounds/boycrying.mp3"
    scold_path = "sounds/crisis.mp3"
    
    # 2. 播放男童哭聲
    if os.path.exists(cry_path):
        st.audio(cry_path, format="boycrying.mp3", loop=False, autoplay=True)
    else:
        st.warning(f"找不到男童哭聲檔案：{cry_path}")
        
    # 3. 同時播放媽媽罵人聲（兩個 st.audio 同時呼叫，瀏覽器會自動混音並行）
    if os.path.exists(scold_path):
        st.audio(scold_path, format="sounds/crisis.mp3", loop=False, autoplay=True)
    else:
        st.warning(f"找不到媽媽罵人聲檔案：{scold_path}")


# ─── 啟動背景繁忙環境音（隨時並行） ───
play_background_ambient()


# ─── 側邊欄：呈現病人現況與病歷摘要 ───
with st.sidebar:
    st.header("📋 病人基本資料")
    meta = CASE_DATA.get("case_meta", {})
    p_name = meta.get("patient_name", "匿名男童 (6 y/o)")
    p_gender = meta.get("gender", "Male")
    
    st.subheader(f"{p_name} ({p_gender})")
    st.write(f"**主訴與情境：**\n{meta.get('scenario', '')}")
    
    # 🖼️ 圖片放置點 1：情境示意圖
    st.image(
        "pediatric_scene.jpg", 
        use_container_width=True
    )
    
    st.divider()
    
    st.header("🌡️ 初始生命徵象 (Vitals)")
    vitals = CASE_DATA.get("vitals_initial", {})
    st.markdown(f"""
    - **血壓 (BP):** {vitals.get('BP', '')}
    - **心跳 (HR):** <span style='color:orange; font-weight:bold;'>{vitals.get('HR', '')}</span>
    - **呼吸 (RR):** {vitals.get('RR', '')}
    - **血氧 (SpO2):** {vitals.get('SpO2', '')}
    - **體溫 (BT):** <span style='color:red; font-weight:bold;'>{vitals.get('BT', '')}</span>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("🩻 理學檢查焦點 (PE)")
    pe = CASE_DATA.get("pe_results", {})
    st.markdown(f"""
    - **腹部觸診:** {pe.get('Abdomen', '')}
    - **觸診細節:** {pe.get('Palpation_Details', '')}
    - **特殊徵象:** <span style='color:red; font-weight:bold;'>{pe.get('Special_Sign', '')}</span>
    """, unsafe_allow_html=True)
    
    # 🖼️ 圖片放置點 2：醫學解剖示意圖
    st.image(
        "peds_ct.jpg",  
        use_container_width=True
    )

# ─── STREAMLIT 聊天記憶庫初始化 ───
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "（周圍傳來急診廣播與推床吵雜聲）醫師您好，我是負責照顧這位 6 歲男童的護理師。病人目前躺在病床上縮成一團陣發性哭鬧，皮膚彈性稍差。請問您有什麼進一步的醫囑指示嗎？"}
    ]
if "round_count" not in st.session_state:
    st.session_state.round_count = 0

# 顯示歷史聊天訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ─── 🤖 本機邏輯模擬器（小兒急診劇本） ───
def local_pediatric_simulator(user_text):
    text = user_text.lower()
    st.session_state.round_count += 1
    
    trigger_crisis_sound = False
    response_text = ""

    # 規則 4：拒絕引導
    if any(q in text for q in ["建議", "怎麼辦", "該做什麼", "你覺得", "有什麼想法"]):
        response_text = "醫師，我需要您明確的醫囑才能執行處置，請告訴我下一步的處置指示。"

    # 規則 2：醫囑明確性檢查與病歷對應
    elif "點滴" in text or "iv" in text or "fluid" in text:
        if any(w in text for w in ["d5", "d10", "ns", "saline", "water"]) and any(f in text for f in ["ml", "qd", "流速", "run"]):
            response_text = "收到，點滴已點上。目前男童心跳 110 次/分，血壓 100/60 mmHg，脫水狀況稍微改善。"
        else:
            response_text = "請問醫師，點滴要用什麼水？流速要開多少？（男童目前體重 20 公斤）"
            
    elif "開刀" in text or "手術" in text or "or" in text:
        response_text = "收到，那請問目前需要開始 NPO（禁食）嗎？有需要先照會小兒外科嗎？"
        
    elif "止痛" in text or "pain" in text or "acetaminophen" in text:
        response_text = "請問要開哪一種止痛藥？劑量和給藥途徑（口服/靜脈）為何？"
        
    elif "抽血" in text or "cbc" in text or "crp" in text or "驗尿" in text or "ua" in text:
        response_text = f"收到，已完成採檢送驗。以下為檢驗數據回報：\n\n**【血液與尿液檢驗報告】**\n- CBC/DC & CRP: {CASE_DATA['diagnostic_results']['CBC_DC_CRP']}\n- Urine Analysis: {CASE_DATA['diagnostic_results']['UA']}"
        
    elif "超音波" in text or "pocus" in text or "echo" in text:
        response_text = f"已聯絡床邊超音波評估。報告顯示：\n\n{CASE_DATA['diagnostic_results']['POCUS_Raw_Report']}"
        
    elif "電腦斷層" in text or "ct" in text:
        response_text = f"已送往放射科完成電腦斷層。關鍵決策報告如下：\n\n{CASE_DATA['diagnostic_results']['Abdominal_CT_Angiography']}"
        
    elif "會診" in text or "照會" in text or "外科" in text:
        response_text = f"已照會小兒外科醫師，當前照會回覆如下：\n\n{CASE_DATA['diagnostic_results']['Consult_Pediatric_Surgeon']}"
        
    else:
        response_text = "收到醫師醫囑。請下達詳細的規格指令（如點滴水別流速、藥物劑量、或安排特定影像檢查）。"

    # 規則 3：生理數據惡化 + 哭聲 + 家屬痛罵隱形施壓（對話達 3 輪以上）
    if st.session_state.round_count >= 3:
        response_text = (
            "😫 **（⚠️ 男童開始劇烈嚎哭，家屬情緒爆發）**\n\n"
            "「**弟弟哇哇大哭：** 媽媽我好痛！！😭😭😭...」\n"
            "「**家屬憤怒咆哮：** 醫師！🤬🤬😤🤬？！」\n\n"
            "**【目前病患狀態】**：男童因劇烈疼痛臉色發青、全身冷汗，心跳飆升至 130 bpm。醫師，請立刻處置！"
        )
        trigger_crisis_sound = True  # 觸發兒童哭鬧與現場混亂音效

    return response_text, trigger_crisis_sound


# ─── 住院醫師（使用者）輸入區 ───
# 🌟 關鍵保護：全檔案唯一確定的 chat_input，並加上專屬 key
if user_input := st.chat_input("請輸入緊急醫囑指示...", key="pediatric_unique_chat_key"):
    
    # 1. 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 2. 透過本機模擬器計算回應
    full_response, trigger_crisis = local_pediatric_simulator(user_input)

    # 3. 顯示 AI 模擬回應
    with st.chat_message("model"):
        st.markdown(full_response)
        
    # 4. 儲存至記憶庫維持畫面
    st.session_state.messages.append({"role": "model", "content": full_response})
    
    # 5. 🎛️ 疊加混音：如果達到第 3 輪，在繁忙背景音之上疊加哭喊音效！
    if trigger_crisis:
        play_crisis_sounds()