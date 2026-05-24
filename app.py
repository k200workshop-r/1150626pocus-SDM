import os
import streamlit as st
from google import genai
from google.genai import types

# 匯入病歷資料
from patient_case import CASE_DATA

# ─── STREAMLIT 網頁基礎設定 ───
st.set_page_config(page_title="臨床病歷決策模擬", layout="wide")
st.title("🩺 臨床情境模擬：你與護理師互動視窗")

# ─── GEMINI API 客戶端初始化 ───
# 優先從環境變數讀取，若找不到則使用您提供的 Key 備份
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyC-vvhA6qZtBde-UB4HcC1aDnqDhJdnn1I")
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.5-flash"

# ─── 側邊欄：呈現病人現況與病歷摘要 ───
with st.sidebar:
    st.header("📋 病人基本資料")
    meta = CASE_DATA["case_meta"]
    st.subheader(f"{meta['patient_name']} ({meta['gender']})")
    st.write(f"**主訴與情境：**\n{meta['scenario']}")
    
    st.divider()
    
    st.header("🌡️ 初始生命徵象 (Vitals)")
    vitals = CASE_DATA["vitals_initial"]
    st.markdown(f"""
    - **血壓 (BP):** {vitals['BP']}
    - **心跳 (HR):** {vitals['HR']}
    - **呼吸 (RR):** {vitals['RR']}
    - **血氧 (SpO2):** {vitals['SpO2']}
    - **體溫 (BT):** {vitals['BT']}
    """)
    
    st.divider()
    
    st.header("🩻 理學檢查焦點 (PE)")
    pe = CASE_DATA["pe_results"]
    st.markdown(f"""
    - **腹部觸診:** {pe['Abdomen']}
    - **觸診細節:** {pe['Palpation_Details']}
    - **特殊徵象:** {pe['Special_Sign']}
    """)

# ─── 建立 AI 系統提示詞 (System Instruction) ───
# 將 patient_case.py 的所有數據結構化地塞入 System Instruction，讓 AI 護理師完全掌握這個案例的所有檢查結果與答案
system_instruction_text = f"""
# Role
你是一位資深的急診護理師。此時你正在照顧一位 6 歲因急性腹痛入院的男童。你的任務是與住院醫師（使用者）對話，並執行他所下達的醫囑。

# Clinical Scenario Context & Hidden Case Data
你完整掌握該病患的所有病歷資料與後續檢驗結果（如下所示）。但請記住，除非醫師主動下達相關醫囑、安排相關檢查、或詢問相關數據，否則你絕對不能主動洩漏後續的檢查結果。

- **病患元數據與病歷：** {str(CASE_DATA['case_meta'])}
- **初始生命徵象：** {str(CASE_DATA['vitals_initial'])}
- **理學檢查：** {str(CASE_DATA['pe_results'])}
- **既往病歷紀錄（包含前一班的錯誤診斷）：** {str(CASE_DATA['medical_records'])}
- **臨床檢查快捷對應數據（當醫師安排以下項目時，你可以據此回報結果）：** {str(CASE_DATA['diagnostic_results'])}

# Interaction Rules（嚴格遵守：不引導、不給答案）
1. 嚴格被動：你絕對不能主動提出任何醫療建議、檢查項目或藥物名稱。
2. 醫囑明確性檢查：
   - 若醫師說「打點滴」，你必須回應：「請問醫師，點滴要用什麼水？流速要開多少？」
   - 若醫師說「準備開刀/送手術室」，你必須回應：「收到，那請問目前需要開始 NPO（禁食）嗎？有需要先照會小兒外科嗎？」(僅針對醫師提到的關鍵字進行程序確認，不主動擴展)
   - 若醫師說「先給止痛藥」，你必須回應：「請問要開哪一種止痛藥？劑量和給藥途徑（口服/靜脈）為何？」
3. 狀態回報：
   - 當醫師下達正確且完整的醫囑後，你要客觀回報「執行結果」或從上述「臨床檢查快捷對應數據」中提取「病人當前數據/報告」回報給醫師。
   - 例如醫師下達正確流速的點滴後，回報：「點滴已點上。目前男童心跳 110 次/分，血壓 100/60 mmHg。」
4. 拒絕引導：如果醫師問你「你覺得現在該做什麼？」或「你有什麼建議？」，你必須客觀回答：「醫師，我需要您明確的醫囑才能執行處置，請告訴我下一步的指示。」
"""

# ─── STREAMLIT 聊天記憶庫初始化 ───
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "醫師您好，我是負責照顧這位 6 歲男童的護理師。病人目前躺在病床上哭鬧，看起來有輕度脫水。請問您有什麼進一步的醫囑指示嗎？"}
    ]

# 顯示歷史聊天訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── 住院醫師（使用者）輸入區 ───
if user_input := st.chat_input("請輸入醫囑或指示例：安排 CBC 檢查、給予 NPO、打點滴..."):
    
    # 1. 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 2. 轉換歷史對話紀錄為 Gemini 支援的 Contents 格式
    formatted_contents = []
    for msg in st.session_state.messages:
        formatted_contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    # 3. 配置 Gemini 參數 (包含思考模型、Google搜尋、System Instruction)
    tools = [types.Tool(googleSearch=types.GoogleSearch())]
    
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        tools=tools,
        system_instruction=[
            types.Part.from_text(text=system_instruction_text),
        ],
    )

    # 4. 呼叫 API 並以 Stream 串流輸出回覆
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            response_stream = client.models.generate_content_stream(
                model=MODEL_ID,
                contents=formatted_contents,
                config=generate_content_config,
            )
            
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            # 移除最後的輸入游標符號
            response_placeholder.markdown(full_response)
            
            # 5. 儲存 AI 的回覆到記憶庫
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"呼叫 API 時發生錯誤: {e}")