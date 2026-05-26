import os
import time
import streamlit as st

# ─── STREAMLIT 網頁基礎設定 ───
st.set_page_config(page_title="GI 病房臨床情境模擬", layout="wide")
st.title("🩺 臨床情境模擬：內科病房模擬")

# ─── 🔊 音效播放組件 (解鎖自動播放限制版) ───

def play_background_ambient():
    """【聲道 1】在網頁背景持續『循環』播放病房/醫院繁忙的吵雜聲"""
    audio_path = "sounds1/ambient.mp3" 
    if os.path.exists(audio_path):
        st.audio(audio_path, format="sounds1/ambient.mp3", loop=True, autoplay=True)


# ─── ⏱️ 20分鐘倒數計時系統記憶庫初始化 ───
if "start_time" not in st.session_state:
    st.session_state.start_time = None  
if "time_up" not in st.session_state:
    st.session_state.time_up = False    

TOTAL_SECONDS = 20 * 60

# ─── 📋 側邊欄：呈現病人現況、計時器、以及側邊欄圖片 ───
with st.sidebar:
    st.header("⏳ 臨床決策時間")
    timer_placeholder = st.empty()  
    
    if st.session_state.start_time is not None:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, TOTAL_SECONDS - elapsed_time)
        if remaining_time <= 0:
            st.session_state.time_up = True
            
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
    st.write(
        "**病史摘要：**\n"
        "病人過去有糖尿病與 B 型肝炎帶原病史。住院前 7 天開始出現全身黃疸及茶色尿，"
        "並合併腹脹、排氣增加，近一個月內體重不明原因下降約 2–3 公斤。"
    )
    
    # 🖼️ 【圖片放置點 1：側邊欄靜態示意圖】
    # 你可以把底下的網址換成你 GitHub 上的本機圖片路徑（如 "images/patient.jpg"）或任意網路圖片網址
    st.image(
        "clinical_performance.jpg", 
        use_container_width=True
    )
    
    st.divider()
    
    st.header("🌡️ 當前生命徵象 (Vitals)")
    st.markdown("""
    - **意識狀態 (GCS):** E4V5M6 (清楚)
    - **體溫 (BT):** 36.5 °C
    - **血壓 (BP):** 177/98 mmHg
    - **心跳 (HR):** 80 次/分鐘
    """, unsafe_allow_html=True)
    
    st.divider()
    
st.header("理學檢查焦點 (PE)")
    st.markdown("""
    - **眼部檢查:** 鞏膜黃染 (Icteric sclera)
    - **腹部觸診:** 腹部平坦、無壓痛、無反彈痛
    """, unsafe_allow_html=True)
    
    # 🖼️ 【圖片放置點 2：醫學基礎參考圖】
    st.image(
        "structure.jpg", 
        use_container_width=True
    )
# ─── STREAMLIT 聊天記憶庫初始化 ───
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": (
            "病房護理師回報：\n"
            "「醫師你好，我是負責看顧 27 床張先生的護理師。病人是 52 歲男性，過去有糖尿病和 B 肝。這次因為全身發黃、尿液變茶色一個禮拜，診所看過懷疑是急性肝炎，但吃藥沒好轉轉過來的。目前人清醒，沒燒沒痛，但血壓有點高（177/98 mmHg），鞏膜黃染蠻明顯的。"
            "請問醫師，我們接下來第一步要安排什麼處置或影像檢查？」"
        )}
    ]
if "round_count" not in st.session_state:
    st.session_state.round_count = 0

# 顯示歷史聊天訊息（如果歷史訊息裡包含自訂的圖片標記，會在此被渲染）
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # 如果該訊息帶有自訂的圖片欄位，則同步渲染出來
        if "image_url" in msg and msg["image_url"]:
            st.image(msg["image_url"], caption=msg.get("image_caption", ""), width=500)

# ─── 🤖 本機智慧型邏輯模擬器（內建對話動態圖檔觸發機制） ───
def local_clinical_simulator(user_text):
    text = user_text.lower()
    st.session_state.round_count += 1
    
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
        
    response_text = ""
    image_url = None
    image_caption = ""

    # 1. 拒絕引導
    if any(q in text for q in ["建議", "怎麼辦", "該做什麼", "你覺得", "有什麼想法"]):
        response_text = "醫師，這是阻塞性黃疸個案，目前病因尚不明確。我需要你明確的處置醫囑才能執行，請下達下一步明確指示。"

    # 2. 醫囑精確性檢查 (融入 Admission / Progress / Discharge Note 完整臨床軌跡)
    elif "點滴" in text or "iv" in text or "fluid" in text or "輸液" in text:
        if any(w in text for w in ["flomoxef", "抗生素", "ns", "saline", "water"]) and any(f in text for f in ["ml", "qd", "流速", "run", "q8h"]):
            response_text = "好的，目前已為張先生點上點滴，並靜脈給藥。另外，病人有糖尿病病史，目前的急診血糖檢驗值偏高，為 161 mg/dl。"
        else:
            response_text = "請問醫師，點滴水別要開什麼？流速要開多少？（提示：病人有糖尿病病史，目前血糖值為 161 mg/dl。若要給予經驗性抗生素治療，請下達包含藥名、劑量與流速的完整規格指示）。"
            
    elif "電腦斷層" in text or "ct" in text or "影像" in text:
        response_text = (
            "已為您調出 5/1 開立的**【腹部電腦斷層 (Abdomen CT Routine) 報告】**：\n"
            "1. **胰臟病灶**：於胰臟鉤突 (uncinate process) 及胰頭處發現一處邊界不清之低增強結節性病灶 (ill-defined hypoenhancing nodular lesion)，高度疑似胰頭腫瘤（需強烈考慮惡性腫瘤可能）。\n"
            "2. **膽管擴張**：伴隨主胰管擴張、雙側肝內膽管 (IHD) 及總膽管 (CBD) 輕度擴張，符合阻塞性黃疸表現。\n"
            "3. **其餘發現**：右腎小囊腫、攝護腺肥大合併鈣化、主動脈粥狀硬化。請問下一步要安排緊急減黃引流嗎？"
        )
        # 🖼️ 【圖片放置點 3：學員查 CT 時動態跳出的圖片】
        # 你可以換成真實的 Pancreatic Head Tumor CT 圖片路徑
        image_url = "Pancreatic_ct.jpg"
        image_caption = "可見胰頭處結節病灶與上游膽管擴張"
        
    elif "減黃" in text or "引流" in text or "ptcd" in text:
        response_text = "好的！已立刻聯絡放射科。5/2 已順利為病人執行 **PTCD（經皮經肝膽道引流術）** 緊急減黃，目前順利引流出茶色膽汁，黃疸與腹脹症狀有稍微緩解。請問後續是否要在 5/4 進一步安排內視鏡介入處置？"
        
    elif "內視鏡" in text or "ercp" in text or "支架" in text or "erbd" in text:
        response_text = (
            "好的，已於 5/18 順利送至內視鏡室完成 **ERCP**：\n"
            "- 順利在 distal CBD 放置塑膠支架 (ERBD, 8.5 Fr x 7 cm) 進行引流。\n"
            "- 已同步在遠端總膽管狹窄處完成**膽道內切片 (Endobiliary biopsy x 3#)** 送檢，目前常規監測術後狀況。"
        )
        
    elif "病理" in text or "切片" in text or "報告" in text or "biopsy" in text:
        response_text = "醫師，5/7 內視鏡膽道切片病理報告（Biopsy Pathology）結果回報了：檢體顯微鏡下證實為 **Adenocarcinoma（腺癌）**。目前確診為胰臟腺癌，請問醫師是否要安排進一步的癌症期別分期（Staging）影像檢查？"
        
    elif "磁振造影" in text or "mri" in text or "分期" in text or "staging" in text:
        response_text = (
            "報告醫師，5/9 已完成 **胰臟核磁共振 (Pancreas MRI)** 以及胸部 CT。關鍵報告如下：\n"
            "- **遠端擴散**：胸部 X 光及胸部 CT 無明顯遠端肺轉移。\n"
            "- **🚨 嚴重發現**：MRI 證實胰臟鉤突惡性腫瘤，但肝臟內部已出現**多發性肝轉移 (Multiple hepatic metastasis)**！\n"
            "目前臨床分期確定為晚期癌症。（💡 護理師已將 MRI 分期影像切換至主螢幕如下）"
        )
        # 🖼️ 【圖片放置點 4：學員查 MRI 報告時動態跳出的圖片】
        # 你可以換成真實的 Liver Metastasis MRI 圖片路徑
        image_url = "Liver_metastases_MRI.jpg"
        image_caption = "張先生的核磁共振影像：肝臟內可見多發性轉移性結節性病灶"
        
    elif "會診" in text or "照會" in text or "外科" in text or "gs" in text or "腫瘤" in text:
        response_text = "已召集一般外科與血液腫瘤科會診。醫師評估後回覆：因合併多發性肝轉移，目前無法進行根除性手術（如 Whipple 手術），建議由放腫科接手評估全身性化學治療。請問醫師，需要安排時間向病人及家屬解釋病情嗎？"
        
    elif "轉院" in text or "aad" in text or "台大" in text or "出院" in text:
        response_text = "將協助辦理 **AAD（自動出院）**。病歷摘要與病理報告已印出，轉診目的地開立為台大醫院，已交代家屬相關注意事項，張先生已由太太陪同離院辦理手續。"
        
    else:
        response_text = "病人目前有嚴重的阻塞性黃疸，請確認下一步明確的處置指令（例如：安排影像檢查 CT、下達精確的點滴水別與流速、追蹤病理切片結果、或安排 MRI 進行 Staging 分期評估）。"

    # 3. 高壓隱形施壓機制（當對話達 3 輪以上，家屬情緒全面引爆）
    if st.session_state.round_count >= 3:
        response_text = (
            "😫 **（⚠️ 病人與家屬得知電腦斷層高度懷疑胰頭惡性腫瘤，且 MRI 證實多發性肝轉移後，情緒全面崩潰）**\n\n"
            "「**張先生眼眶泛紅痛哭：** 怎麼會這樣...我只是皮膚變黃、肚子有點脹而已...怎麼一到你們大醫院檢查，就直接跟我說已經末期擴散了、不能開刀了...」\n"
            "「**太太焦慮憤怒：** 醫師！前天診所分明說只是急性肝炎，吃藥就會好！為什麼來這裡住幾天院，就變成癌症末期？！到底能不能治？！我們要求立刻辦自動出院（AAD），我們要轉去台大醫院找名醫看！現在立刻幫我們弄轉院手續，一分鐘都不要拖！」\n\n"
            "**【目前病患狀態】**：家屬防衛心極高，拒絕本院任何進一步處置，強烈要求簽字 AAD 轉診台大。醫師，請執行高階醫病溝通與後續離院/轉診處置醫囑！"
        )
        # 🖼️ 【圖片放置點 5：第三輪高壓崩潰時，可以同步秀出轉診/AAD文件的示意圖】
        image_url = "AAD.jpg"

    return response_text, image_url, image_caption


# ─── 住院醫師（使用者）輸入區 ───
if st.session_state.time_up:
    st.chat_input("⏱️ 20分鐘評估時間已結束！無法再下達醫囑。", disabled=True, key="gi_nurse_chat_key")
else:
    if user_input := st.chat_input("請輸入緊急醫囑指示...", key="gi_nurse_chat_key"):
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # 透過智慧型本機模擬器計算回應（包含動態圖檔）
        full_response, img_url, img_caption = local_clinical_simulator(user_input)

        # 顯示護理師文字回應
        with st.chat_message("model"):
            st.markdown(full_response)
            # 如果這一步有觸發動態圖檔，立刻在對話框下方渲染
            if img_url:
                st.image(img_url, caption=img_caption, width=500)
            
        # 儲存至記憶庫，包含圖片資訊，確保 rerun 後畫面不會丟失圖片
        st.session_state.messages.append({
            "role": "model", 
            "content": full_response,
            "image_url": img_url,
            "image_caption": img_caption
        })
        
        # 音效自動播放控制（背景病房雜音）
        play_background_ambient()  
            
        st.rerun()