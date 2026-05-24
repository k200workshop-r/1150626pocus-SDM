import os
import streamlit as st

# 匯入 6 歲男童個案病歷資料
from patient_case import CASE_DATA

# ─── STREAMLIT 網頁基礎設定 ───
st.set_page_config(page_title="小兒急診臨床情境模擬", layout="wide")
st.title("🩺 臨床情境模擬：你與急診護理師互動視窗")

# ─── 🔊 音效播放組件 ───

def play_background_ambient():
    """【聲道 1】在網頁背景持續『循環』播放急診室繁忙的吵雜聲 (Ambient)"""
    audio_path = "sounds/er_room.mp3" 
    if os.path.exists(audio_path):
        st.audio(audio_path, format="sounds/er_room.mp3", loop=True, autoplay=True)


def play_crisis_sounds():
    """【聲道 2】當對話達 3 輪時，『同時重疊』播放男童哭聲與媽媽罵人聲"""
    cry_path = "sounds/boycrying.mp3"
    scold_path = "sounds/crisis.mp3"
    
    if os.path.exists(cry_path):
        st.audio(cry_path, format="sounds/boycrying.mp3", loop=False, autoplay=True)
    if os.path.exists(scold_path):
        st.audio(scold_path, format="sounds/crisis.mp3", loop=False, autoplay=True)


# ─── 側邊欄：呈現病人現況與病歷摘要 ───
with st.sidebar:
    st.header("📋 病人基本資料")
    meta = CASE_DATA.get("case_meta", {})
    p_name = meta.get("patient_name", "匿名男童 (6 y/o)")
    p_gender = meta.get("gender", "Male")
    
    st.subheader(f"{p_name} ({p_gender})")
    
    # ─── 💡 臨床情境更新（加入重返急診病史） ───
    st.error("⚠️ 高風險個案：72小時內重返急診 (ER Return Visit)")
    st.write(
        "**病史摘要：**\n"
        "男童 2 天前因發燒與上腹痛至本院急診，當時初步懷疑為「急性胃腸炎」。\n\n"
        "**【前次急診處置】**：\n"
        "- **靜脈輸液**：給予小兒維持液 **D5 0.45%S** 依體重穩定滴注，以校正因嘔吐帶來的脫水。\n"
        "- **症狀緩解藥物**：當場給予肛門塞劑 **Acetaminophen (退燒)** 與靜脈注射 **Metoclopramide (Primperan, 止吐)**。\n\n"
        "病童在急診觀察後發燒漸退、嘔吐緩解，隨即辦理離院。當時急診醫師開立了兒科常用的腸胃炎口服藥物帶回家服用，包含：\n"
        "1. **Acetaminophen syrup (安佳熱糖漿)**：發燒或腹痛時症狀緩解使用。\n"
        "2. **Gascon (胃爾康)**：減輕腸胃脹氣與痙攣絞痛。\n"
        "3. **Smecta (舒腹達散劑)**：吸附腸道病菌與保護腸胃黏膜。\n\n"
        "**【本次重返主訴】**：\n"
        "然而返家後症狀完全沒有好轉，上述口服藥物幾乎吃進去就吐出來。昨晚開始腹痛位置明顯**「由上腹部轉移至右下腹」**，痛感轉為持續性的劇烈撕裂痛，"
        "並伴隨反覆高燒（>39°C）與畏寒。今天病童已痛到完全無法行走，是由焦慮的家屬抱著再次緊急衝入急診。"
    )   
    # 🖼️ 圖片放置點 1
    st.image(
        "pediatric_scene.jpg", 
        use_container_width=True
    )
    
    st.divider()
    
    st.header("🌡️ 當前生命徵象 (Vitals)")
    vitals = CASE_DATA.get("vitals_initial", {})
    st.markdown(f"""
    - **血壓 (BP):** {vitals.get('BP', '')}
    - **心跳 (HR):** <span style='color:red; font-weight:bold;'>{vitals.get('HR', '')} bpm</span> (明顯心跳過速)
    - **呼吸 (RR):** {vitals.get('RR', '')}
    - **血氧 (SpO2):** {vitals.get('SpO2', '')}
    - **體溫 (BT):** <span style='color:red; font-weight:bold;'>39.2 °C</span> (持續高燒)
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("🩻 理學檢查焦點 (PE)")
    pe = CASE_DATA.get("pe_results", {})
    st.markdown(f"""
    - **腹部觸診:** {pe.get('Abdomen', '')}
    - **觸診細節:** {pe.get('Palpation_Details', '')}
    - **特殊徵象:** <span style='color:red; font-weight:bold;'>{pe.get('Special_Sign', '')}</span>
    """, unsafe_allow_html=True)
    
    # 🖼️ 圖片放置點 2
    st.image(
        "peds_echo.jpg", 
        use_container_width=True
    )

# ─── STREAMLIT 聊天記憶庫初始化 ───
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": (
            "護理師回報：\n"
            "「醫師，這個 6 歲弟弟是**兩天前才來過急診的 Return 個案**！前天打過點滴退燒後離院，但家屬說回去根本沒有好，反而越來越燒、肚子痛到碰都不能碰，剛剛一量體溫 39.2 度，心跳到 130 幾下。"
            "弟弟現在躺在床上整個人縮在一起，皮膚彈性很差、嘴唇很乾。家屬非常焦慮而且臉色很難看，我們必須小心可能是闌尾炎破裂引發腹膜炎（Peritonitis）。請問您要先開立什麼明確的醫囑？」"
        )}
    ]
if "round_count" not in st.session_state:
    st.session_state.round_count = 0

# 顯示歷史聊天訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ─── 🤖 本機邏輯模擬器（重返急診高壓版） ───
def local_pediatric_simulator(user_text):
    text = user_text.lower()
    st.session_state.round_count += 1
    
    trigger_crisis_sound = False
    response_text = ""

    # 規則 4：拒絕引導
    if any(q in text for q in ["建議", "怎麼辦", "該做什麼", "你覺得", "有什麼想法"]):
        response_text = "（護理師神色凝重）醫師，這是兩天內重返急診的個案，病況變化可能很快，我需要您明確的處置醫囑才能執行，請下達下一步指示。"

    # 規則 2：醫囑明確性檢查與病歷對應
    elif "點滴" in text or "iv" in text or "fluid" in text:
        if any(w in text for w in ["d5", "d10", "ns", "saline", "water"]) and any(f in text for f in ["ml", "qd", "流速", "run"]):
            response_text = "收到，因為前天已經打過點滴，今天病人明顯有 Severe 脱水跡象。兩條大口徑 IV 已重新建立，輸液大量灌注中。目前男童心跳稍微降至 118 次/分，血壓 98/58 mmHg。"
        else:
            response_text = "（護理師提醒）醫師，病人前天打過點滴回去還是一直吐、脫水很厲害，這次點滴水別要用什麼？流速要開多少？（男童體重 20 公斤）"
            
    elif "抗生素" in text or "antibiotic" in text:
        response_text = "收到，高度懷疑腹內感染/腹膜炎。請問要開立哪一種小兒抗生素？劑量與給藥途徑（IV/PO）為何？"

    elif "開刀" in text or "手術" in text or "or" in text:
        response_text = "收到，懷疑 Appendix Rupture 準備手術。請問目前需要開始嚴格 NPO（禁食空腹）嗎？有需要先緊急照會小兒外科嗎？"
        
    elif "止痛" in text or "pain" in text or "acetaminophen" in text:
        response_text = "請問要開哪一種止痛藥？前天開的口服退燒止痛藥返家後似乎壓不住，這次要改為靜脈注射（IV）嗎？劑量為何？"
        
    elif "抽血" in text or "cbc" in text or "crp" in text or "驗尿" in text or "ua" in text:
        response_text = f"收到，已立刻優先採檢送驗。以下為重返急診的最新檢驗數據（WBC與CRP顯著飆高）：\n\n**【血液與尿液檢驗報告】**\n- CBC/DC & CRP: {CASE_DATA['diagnostic_results']['CBC_DC_CRP']}\n- Urine Analysis: {CASE_DATA['diagnostic_results']['UA']}"
        
    elif "超音波" in text or "pocus" in text or "echo" in text:
        response_text = f"已聯絡床邊超音波評估。報告顯示闌尾明顯腫脹且周圍有液體聚積（Fluid accumulation）：\n\n{CASE_DATA['diagnostic_results']['POCUS_Raw_Report']}"
        
    elif "電腦斷層" in text or "ct" in text:
        response_text = f"已啟動綠色通道送往放射科完成電腦斷層。關鍵報告如下：\n\n{CASE_DATA['diagnostic_results']['Abdominal_CT_Angiography']}"
        
    elif "會診" in text or "照會" in text or "外科" in text:
        response_text = f"已十萬火急照會小兒外科醫師，當前照會回覆如下（請確認是否完成 NPO 與備血）：\n\n{CASE_DATA['diagnostic_results']['Consult_Pediatric_Surgeon']}"
        
    else:
        response_text = "請醫師下達明確的醫囑（如點滴水別與流速、經驗性抗生素、或安排緊急影像檢查）。"

    # 規則 3：生理數據惡化 + 哭聲 + 家屬痛罵隱形施壓（對話達 3 輪以上）
    if st.session_state.round_count >= 3:
        response_text = (
            "😫 **（⚠️ 男童腹痛突發加劇並開始劇烈嚎哭，家屬情緒徹底失控咆哮）**\n\n"
            "「**弟弟哇哇大哭：** 媽媽！！😭😭😭...不要碰我...」\n"
            "「**家屬憤怒大罵：** 🤬🤬😤🤬」\n\n"
            "**【目前病患狀態】**：男童因劇烈反跳痛（Rebound tenderness）整個人蜷曲抽搐、冷汗直流，心跳飆升至 142 bpm，血壓開始有敗血性休克早期跡象（90/50 mmHg）。醫師，請立刻下達決定性處置！"
        )
        trigger_crisis_sound = True 

    return response_text, trigger_crisis_sound


# ─── 住院醫師（使用者）輸入區 ───
if user_input := st.chat_input("請輸入緊急醫囑指示...", key="pediatric_perfect_chat_key"):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    full_response, trigger_crisis = local_pediatric_simulator(user_input)

    with st.chat_message("model"):
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "model", "content": full_response})
    
    # ─── 🎛️ 音效自動播放控制 ───
    play_background_ambient()  # 第一句輸入後解鎖並播放背景音
    
    if trigger_crisis:
        play_crisis_sounds()  # 第三輪時同時疊加哭聲與家屬責罵聲