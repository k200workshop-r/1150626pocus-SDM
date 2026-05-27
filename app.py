import os
import time
import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from streamlit_autorefresh import st_autorefresh

# ─── STREAMLIT 網頁基礎設定 ───
st.set_page_config(page_title="GI 病房臨床情境模擬", layout="wide")
st.title("🩺 臨床情境模擬：內科病房")

# ─── ⏱️ 20分鐘倒數計時系統記憶庫初始化 ───
if "start_time" not in st.session_state:
    st.session_state.start_time = None  # 紀錄開始倒數的時間點
if "time_up" not in st.session_state:
    st.session_state.time_up = False    # 標記時間是否用盡
if "round_count" not in st.session_state:
    st.session_state.round_count = 0    # 計算累積對話回合數

TOTAL_SECONDS = 20 * 60  # 20 分鐘 (1200秒)

# 🔄 倒數計時啟動後，開啟背景每秒自動刷新機制，確保時間雷打不動地持續倒數
if st.session_state.start_time is not None and not st.session_state.time_up:
    st_autorefresh(interval=1000, key="timer_counter")


# ─── 🔄 重置新回合的專用函式 ───
def reset_simulation():
    """清除歷史紀錄與計時器，重置模擬狀態"""
    st.session_state.start_time = None
    st.session_state.time_up = False
    st.session_state.round_count = 0
    st.session_state.messages = [
        {
            "role": "model", 
            "content": (
                "病房護理師回報：\n"
                "「醫師你好，我是負責看顧 27 床張先生的護理師。病人是 52 歲男性，過去有糖尿病和 B 肝。這次因為全身發黃、尿液變茶色一個禮拜，診所看過懷疑是急性肝炎，但吃藥沒好轉轉過來的。目前人清醒，沒燒沒痛，但血壓有點高（177/98 mmHg），鞏膜黃染蠻明顯的。請問醫師，我們接下來第一步要安排什麼處置或影像檢查？」"
            ),
            "image_url": None,
            "image_caption": None
        }
    ]


# ─── 🗄️ Pydantic 結構化輸出定義 ───
class NurseResponse(BaseModel):
    response_text: str = Field(description="在此填入護理師依據行為準則冷靜回應或反問的文字（支援 Markdown）")
    trigger_crisis: bool = Field(description="當學員處置延誤或進入家屬情緒崩潰情境時為 true，其餘為 false")
    image_url: str = Field(default=None, description="需要跳出的醫學影像網址（CT 或 MRI），無則填 None")
    image_caption: str = Field(default=None, description="影像圖說與臨床 Findings 描述，無則填 None")


# ─── 🤖 Google AI Studio API 呼叫核心 ───
def call_gemini_jaundice_api(user_message: str) -> NurseResponse:
    """串接最新 Google GenAI SDK (gemini-2.5-pro)"""
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # 完整融入 4 大臨床互動鐵律與黃疸個案完整病歷數據庫
    system_instruction = """# Role
你是一位在醫學中心腸胃內科病房工作多年的資深專科護理師 （NP）。說話冷靜、講求醫療專業。你不會主動引導住院醫師，一切以醫師親口下達的指令（醫囑）為準。

# Scenario Context (52-year-old Male Case Data)
- 病人背景：52 歲男性，糖尿病及 B 型肝炎帶原者。
- 主訴/現病史：住院前 7 天全身黃疸、尿液呈茶色，合併腹脹、排氣增加，近一個月體重下降 2-3 公斤。診所曾懷疑急性肝炎，給藥無效且黃疸持續惡化，轉至本院急診收治住院。
- 初始生命徵象：GCS E4V5M6, 體溫 36.5°C, 血壓 177/98 mmHg, 脈搏 80 次/分, 呼吸 18 次/分, SpO₂ 100% (room air)。
- 身體檢查 (PE)：鞏膜黃染明顯，腹部平坦無壓痛、無反彈痛、無反胃。

[完整病歷檔案庫數據]
- 4/3 Admission Lab: GOT 172, GPT 294, r-GT 1356, Total Bilirubin 9.5 mg/dl, Direct Bilirubin 9.3 mg/dl.
- 4/3 Upper Abdomen CT: 胰臟鉤突及胰頭處見低增強結節性病灶、上游胰管擴張、雙側肝內膽管與總膽管輕度擴張，高度懷疑胰頭惡性腫瘤。
- 4/6 ERCP Report: 執行經內視鏡括約肌切開術 (EST) + 膽道切片 x3 + 放置膽道塑膠支架 (ERBD, 8.5 Fr x 7 cm) 與胰管支架以緩解黃疸。
- 4/9 Pathology: 切片報告證實為胰臟腺癌 (Pancreas adenocarcinoma)。
- 4/11 Pancreas MRI: 證實胰臟鉤突惡性腫瘤伴隨「多發性肝轉移 (Multiple hepatic metastasis)」，屬晚期無法切除之癌症。個案隨後辦理自動出院 (AAD) 轉至台大醫院尋求第二意見。

# Response Rules & Behavior Guidelines (🚨 臨床互動核心鐵律)

1. 嚴格被動 (Strict Passivity)
   - 即使病人黃疸持續惡化或癌症報告出來，妳也絕對不能主動提出任何處置或檢查建議（例如絕對不能主動問：「要幫他排 ERCP 減黃嗎？」、「要不要看切片報告？」、「要照會 GS 外科評估手術嗎？」）。
   - 面對醫師的無效詢問（如：「妳覺得接下來該排什麼檢查？」），妳必須冷靜拒絕並要求明確醫囑：「醫師，病人目前鞏膜黃染明顯，生命徵象穩定，請您開立明確的檢查或處置醫囑，我會立刻為您安排。」

2. 不完整醫囑的應對機制 (防呆反問)
   - 若學員指令模糊、不具體，妳必須以資深 NP 的專業進行精確反問，逼學員補齊劑量、路徑或細節：
     * 醫囑模糊「幫他打點滴」 ── 妳必須反問：「收到，請問目前要點滴輸注什麼常規液體？流速設定多少？病人目前自訴無腹痛、可正常進食。」
     * 醫囑模糊「排個常規腹部電腦斷層（CT）」 ── 妳必須反問：「放射科詢問，病人目前是否已確認 NPO 狀態？另外，今天（5/15）剛送入病房，CRE 報告為 1.3 mg/dl，是否要立刻開立含顯影劑的常規 CT 醫囑？」
     * 醫囑模糊「注意他的血糖和生命徵象」 ── 妳必須反問：「收到，已接上常規量測。請問常規血壓和血糖（病人有 DM 病史）需要設定每幾小時追蹤一次？」
     * 醫囑模糊「準備做內視鏡或聯絡會診」 ── 妳必須反問：「收到，請問目前是要優先聯絡內視鏡室安排 5/18 的 ERCP 進行膽道減黃與切片，還是要優先照會一般外科（GS）或腫瘤科醫師進行評估？」
     * 醫囑模糊「等報告出來再說」 ── 妳必須反問：「收到，請問目前是要優先追蹤 5/18 的 ERCP 膽道切片病理報告，還是 5/23 的胰臟磁振造影（MRI）癌症分期報告？」

3. 面對學員的「純詢問」或「不完整打聽」時的應對
   - 妳絕對不能幫醫師做決定，也不要給予模糊回應。妳必須冷靜地用當前病歷內的生理與檢驗數據回絕他，逼他開出明確醫囑：
     * 當學員問「他目前的黃疸和肝功能數值是多少？」 ── 妳必須回應：「醫師，5/15 抽血報告顯示 GOT 172 U/L, GPT 294 U/L, r-GT 1356 U/L，Total Bilirubin 高達 9.5 mg/dl, Direct Bilirubin 9.3 mg/dl。請下達下一步減黃處置（如安排 PTCD 或 ERCP）或進一步影像檢查的醫囑！」
     * 當學員問「切片報告或 MRI 出來了嗎？是什麼結果？」 ── 妳必須回應：「目前切片與 MRI 報告均已在系統中。醫師，病人生命徵象不穩定或需進行臨床病情解釋，請您明確下達『追蹤切片病理/MRI分期報告』或『進行病情解釋』的明確指令，我會立刻為您調出檔案。」

4. 利用生理數據與家屬情緒惡化進行隱形施壓
   - 如果住院醫師遲遲沒有下達「安排 ERCP 減黃」、「追蹤病理切片報告」以及「執行晚期癌症病情解釋」，隨著對話每進行一輪（超過 3 輪對話），病患黃疸將進行性惡化。
   - 到了第 3 輪以後，家屬與病患得知電腦斷層與 MRI 高度懷疑胰臟腺癌合併多發性肝轉移後，情緒會全面崩潰，強烈要求辦理自動出院（AAD）轉院至台大醫院。此時請將 trigger_crisis 設為 true。

# Interaction & Image Logic (圖片渲染邏輯)
1. 若學員指令明確提及「電腦斷層」、「CT」或「查看 CT 影像」：
   - 將 JSON 中的 image_url 設為 'Pancreatic_ct.jpg'。
   - image_caption 設為 '圖：腹部電腦斷層 (CT) '
   
2. 若學員指令明確提及「核磁共振」、「磁振造影」、「MRI」或「癌症分期」：
   - 將 JSON 中的 image_url 設為 '4.jpg'。
   - image_caption 設為 '圖：胰臟磁振造影 (Pancreas MRI) 顯示胰臟惡性腫瘤已進展至多發性肝轉移 (Hepatic metastasis)。'

3. 若學員下達其他一般處置（如給藥、點滴等），將 image_url 與 image_caption 均設為 null。

# Output Format
必須嚴格遵守以下 JSON 欄位名稱回傳：
{
  "response_text": "妳依據上述規則冷靜給予的反問、拒絕或執行回報文字（支援 Markdown）",
  "trigger_crisis": false,
  "image_url": null,
  "image_caption": null
}
"""

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        temperature=0.35,
        response_mime_type="application/json",
        response_schema=NurseResponse,
        system_instruction=system_instruction
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=f"【學員當前對話輪數：{st.session_state.round_count}】學員指令：{user_message}",
        config=generate_content_config,
    )
    return NurseResponse.model_validate_json(response.text)


# ─── 📋 側邊欄配置 ───
with st.sidebar:
    st.header("⏳ 臨床決策時間")
    timer_placeholder = st.empty()  
    
    # 🔘 手動按鈕清除所有對話紀錄與重來
    if st.button("🔄 開始新回合（清空對話重來）", use_container_width=True):
        reset_simulation()
        st.rerun()

    # ⏱️ 計算並檢查 20 分鐘限時機制
    if st.session_state.start_time is not None:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, TOTAL_SECONDS - elapsed_time)
        
        # ⚡ 20分鐘時間到，自動清除前面所有的歷史紀錄與影像
        if remaining_time <= 0 and not st.session_state.time_up:
            st.session_state.time_up = True
            st.session_state.messages = []  
            st.rerun()
            
        mins, secs = divmod(int(remaining_time), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        if remaining_time > 300:
            timer_placeholder.metric(label="剩餘評估時間", value=time_str)
        else:
            timer_placeholder.metric(label="🚨 警告：時間即將耗盡", value=time_str, delta="-時間危急", delta_color="inverse")
    else:
        timer_placeholder.metric(label="尚未開始計時", value="20:00")

    st.divider()
    st.header("📋 病人基本資料")
    st.subheader("張先生 (52 y/o) (Male)")
    st.write("**病史摘要：**\n糖尿病及 B 肝帶原。因全身發黃、尿液變茶色一個禮拜，由急診收治入院。CRE: 1.3 mg/dl, Total Bilirubin: 9.5 mg/dl。")
    
# ─── 側邊欄圖片防護區 ───
    try:
        st.image("eyes.jpg", caption="病人臨床表徵：鞏膜黃染 (Icteric sclera)", use_container_width=True)
    except Exception:
        # 💡 關鍵修正點（第 180 行）：這裡必須有一行往右縮排 8 個空格的指令，絕對不能留空！
        st.caption("⚠️ [側邊欄參考圖片載入中]")

# ─── 🔄 STREAMLIT 聊天畫面記憶庫初始化 ───
# 💡 檢查點（第 182 行）：這一行 if 必須完全貼齊最左邊（0 個空格），不能縮排！
if "messages" not in st.session_state:
    reset_simulation()

# 顯示歷史對話紀錄
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image_url"):
            try:
                st.image(msg["image_url"], caption=msg.get("image_caption"), width=550)
            except Exception:
                # 💡 關鍵修正點：在第 193 行 except 內部，必須補上這行並往右縮排 16 個空格！
                st.caption("⚠️ [歷史影像下載超時]")

# ─── 住院醫師輸入處理區 ───
# 💡 這一行（第 197 行）是獨立的主線，必須完全靠左（0 個空格），不能縮排！
if st.session_state.time_up:
    st.error("⏱️ 20分鐘評估時間已結束！前方的對話與醫療影像紀錄已自動清除完畢。")
    st.info("💡 請點擊左側面板的「🔄 開始新回合」按鈕重新發起挑戰。")
    st.chat_input("時間已耗盡，請重新開啟新回合。", disabled=True, key="gi_nurse_chat_key")
else:
    if user_input := st.chat_input("請輸入緊急處置或追蹤醫囑...", key="gi_nurse_chat_key"):
        
        # ⚡ 只要學員一輸入第一個指令，立刻啟動 20 分鐘背景倒數計時
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        st.session_state.round_count += 1
            
        # 1. 立即將學員的對話同步到網頁上
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input, "image_url": None, "image_caption": None})
        
        # 2. 串接 API 獲取資深 NP 嚴格被動的回覆
        with st.chat_message("model"):
            with st.spinner("護理師確認醫囑中..."):
                try:
                    ai_output = call_gemini_jaundice_api(user_input)
                    nurse_talk = ai_output.response_text
                    img_url = ai_output.image_url
                    img_caption = ai_output.image_caption
                except Exception as e:
                    nurse_talk = f"⚠️ 護理師正忙於常規照護中，請重新下達明確處置指令。（錯誤提示：{str(e)}）"
                    img_url, img_caption = None, None

            # 3. 雙重防線：若回合計數達 3 輪以上，且未有效處理癌症轉折，強制爆發家屬崩潰 AAD 劇本
            if st.session_state.round_count >= 3 and "AAD" not in user_input and "解釋" not in user_input and "轉院" not in user_input:
                nurse_talk = (
                    "😫 **（⚠️ 病人與家屬得知 4/9 切片報告為 adenocarcinoma 且 4/11 MRI 證實多發性肝轉移後，情緒全面崩潰）**\n\n"
                    "「**張先生眼眶泛紅哀傷：** 怎麼會這樣...我只是皮膚變黃而已...為什麼一檢查就是末期...」\n"
                    "「**太太焦慮：** 醫師！前幾天診所分明說只是急性肝炎！為什麼來住幾天院，就變成癌症末期無法手術？！我們要求立刻辦**自動出院（AAD）**，我們要拿切片跟影像轉去台大醫院找名醫看！現在立刻幫我們弄手續，一分鐘都不要拖！」\n\n"
                    "**【目前病患狀態】**：家屬防衛心極高，拒絕常規住院，強烈要求辦理 AAD 轉診台大。醫師，請執行高階醫病溝通（AAD 說明或備妥轉診資料）！"
                )
                img_url = "Liver_metastases_MRI.jpg"
                img_caption = "圖：4/11 胰臟 MRI 顯示晚期多發性肝轉移惡性病灶"

            # 4. 渲染護理師對話文字與動態觸發的醫學影像
            st.markdown(nurse_talk)
            if img_url:
                try:
                    st.image(img_url, caption=img_caption, width=550)
                except Exception:
                    st.warning("⚠️ [臨床影像加載超時，系統已自動防護攔截，不影響網頁對答]")
                    
        # 5. 打包儲存到歷史紀錄中
        st.session_state.messages.append({
            "role": "model", 
            "content": nurse_talk,
            "image_url": img_url,
            "image_caption": img_caption
        })
        st.rerun()