# patient_case.py

CASE_DATA = {
    "case_meta": {
        "case_id": "PED-2026-001",
        "patient_name": "匿名男童 (6 y/o)",
        "age": 6,
        "gender": "Male",
        "scenario": (
            "6歲男童因急性腹痛並伴隨嘔吐3次，腹痛位置由肚臍周圍轉移至右下腹，從疼痛開始已持續約12小時。"
            "父母主訴病人昨晚開始食慾不振，今天早晨出現低溫發燒與陣發性哭鬧，男童先於家中吞食口服退燒藥後，"
            "症狀仍未緩解，且走路時步態緩慢、身軀微彎，後因腹痛加劇及持續低燒由家長送至急診就醫。"
        )
    },
    
    "vitals_initial": {
        "BP": "108/68 mmHg",
        "HR": "118 bpm",
        "RR": "24 bpm",
        "SpO2": "99% on room air",
        "BT": "38.4°C"
    },
    
    "pe_results": {
        "HEENT": "Throat: mildly injected, no purulent exudate. Neck: Supple, no LAP.",
        "Chest": "Clear, bilateral breathing sounds are symmetric. No wheezing or rales.",
        "Heart": "Tachycardia, regular rhythm, no murmur.",
        "Abdomen": "Slightly distended, Hyperactive bowel sounds. Tenderness over RLQ, McBurney Point (+).",
        "Palpation_Details": (
            "Voluntary guarding noted during crying; abdomen becomes soft when the child is distracted by tablets. "
            "Rebound tenderness is equivocal due to patient’s general irritability. Mild involuntary muscle guarding felt upon deep palpation."
        ),
        "Special_Sign": "Jumping test (+) - induces sharp, localized RLQ pain. Hunched gait noted when walking."
    },
    
    "medical_records": {
        "admission_note": """
【Admission Note】
Date: 2026-05-06 10:00
Chief Complaint: Abdominal pain and vomiting x3 for 12 hours.

Present Illness:
- 6 y/o male with history of recent URI (sore throat, rhinorrhea) 3 days ago.
- Abdominal pain started as periumbilical discomfort, then migrated to RLQ.
- Associated with anorexia and low-grade fever.
- Physical activity limited by pain; hunched gait noted.
- History of sibling having similar GI symptoms (diarrhea/vomiting) last week.

Physical Examination:
- Vital Signs: T: 38.4°C, HR: 118 bpm, RR: 24 bpm, BP: 108/68 mmHg.
- Abdomen: Slightly distended, Hyperactive bowel sounds.
- Palpation: Tenderness over RLQ, McBurney Point (+). Voluntary guarding noted during crying; abdomen becomes soft when the child is distracted by tablets. Rebound tenderness is equivocal due to patient’s general irritability.
- Special Sign: Jumping test (+) but patient also complains of generalized discomfort.

Initial Assessment:
1. Mesenteric Adenitis: Highly suspected due to recent URI prodrome and presence of hyperactive bowel sounds.
2. Acute Gastroenteritis (AGE): R/O viral origin given the family history.
3. Acute Appendicitis: To be ruled out, though the migration of pain is non-specific in pediatric viral syndromes.

Initial Plan:
- NPO with IV fluid hydration.
- Lab: CBC/DC, CRP, U/A.
- Medication: Symptomatic relief (Antipyretics, Anti-emetics).
""",

        "progress_note": """
【Progress Note】
Date: 2026-05-06 16:00
Subjective:
- Pain intensity decreased after Acetaminophen.
- Mother reports child slept for 2 hours. No more vomiting.

Objective:
- Lab results: WBC: 11,500/uL, Seg: 70%, CRP: 14 mg/L. (Non-specific mild elevation).
- POCUS (performed by resident): Multiple enlarged lymph nodes (up to 1.2 cm) in the RLQ. Appendix is not clearly visualized, but no significant free fluid in the pelvic cavity.
- Physical Exam: Abdomen remains soft. RLQ tenderness is still present but less intense.

Assessment:
- Mesenteric Adenitis: Supported by POCUS findings (lymphadenopathy) and recent URI history. The patient shows clinical improvement with conservative management.

Plan:
- Trial of clear liquid diet.
- Prepare for discharge if oral intake is tolerated.
""",

        "discharge_note": """
【Discharge Note】
Date: 2026-05-06 20:00
Discharge Diagnosis:
1. Mesenteric Adenitis (腸繫膜淋巴腺炎)

Brief Clinical Course:
- A 6-year-old male presented with RLQ pain and vomiting. Initial concern for appendicitis was raised due to McBurney point tenderness.
- However, given the recent URI history, non-toxic appearance after hydration, and POCUS findings showing prominent mesenteric lymph nodes without evidence of a dilated appendix, the diagnosis was shifted to Mesenteric Adenitis.
- The patient's inflammatory markers (WBC, CRP) were only mildly elevated, inconsistent with perforated appendicitis.
- Symptomatic improvement was achieved with IV fluids and antipyretics. Patient tolerated oral intake in the ED observation ward.

Discharge Medication:
- Acetaminophen 250mg q6h PRN.
- Probiotics (Biofermin) 1 tab TID.

Follow-up Plan:
- Pediatric outpatient clinic in 3 days.
- ER return if: Persistent high fever, rebound tenderness, or progressive abdominal rigidity.
"""
    },
    
    # ─── 臨床檢查快捷鍵對應數據 (住院醫師查了才給，或AI根據此回答) ───
    "diagnostic_results": {
        "CBC_DC_CRP": "WBC: 11,500/uL, Seg: 70%, Lym: 22%, Hb: 12.8 g/dL, PLT: 280,000/uL. CRP: 14 mg/L.",
        "UA": "Urine analysis: Color: Straw-yellow, WBC: 0-2/HPF, RBC: 1-2/HPF, Nitrite: Negative, Ketone: (2+) (提示脫水/飢餓).",
        "POCUS_Raw_Report": "Multiple lymph nodes in RLQ, largest 1.2 x 0.6 cm. The appendix is obscured by overlying bowel gas, poorly visualized.",
        "Recheck_Vitals_After_6H": "T: 38.2°C, HR: 110 bpm, RR: 22 bpm, BP: 105/65 mmHg. (發燒與心跳無明顯改善)",
        "Abdominal_CT_Angiography": (
            "【腹部電腦斷層報告 - 關鍵決策】\n"
            "Findings: A distended, non-compressible blind-ended tubular structure measured 7.5 mm in diameter "
            "is noted at the RLQ, with significant wall enhancement and periappendiceal fat stranding. "
            "Multiple enlarged mesenteric lymph nodes are also present.\n"
            "Impression: Acute Appendicitis co-existing with reactive Mesenteric Adenitis. (確診：急性闌尾炎伴隨反應性淋巴腺炎)"
        ),
        "Consult_Pediatric_Surgeon": "小兒外科照會回覆：『理學檢查仍有局部反跳痛與腹肌防禦，Jumping test強烈陽性，且CT已證實Appendicitis。建議安排急診手術（Appendectomy）。』"
    },
    
    # ─── 提供給後台 AI 導師 (Debriefing) 用於結算打分的標準答案 ───
    "hidden_truth": {
        "pre_班_error": "將「急性闌尾炎」誤診為「腸繫膜淋巴腺炎」，並草率計畫讓病人出院。",
        "correct_diagnosis": "Acute Appendicitis (急性闌尾炎)",
        "missed_clues": [
            "1. 轉移性腹痛（肚臍周圍轉移至右下腹）是闌尾炎的極典型表徵，不應單純因URI歷史而忽視。",
            "2. Jumping test (+) 是強烈的腹膜刺激徵象（Peritoneal sign），比嬰幼兒哭鬧時的壓痛更具診斷價值。",
            "3. POCUS 顯示『Appendix is not clearly visualized（闌尾看不清）』在小兒科非常常見，這並非排除闌尾炎的依據，僅代表『未看清』。",
            "4. 雖然 WBC/CRP 僅輕微上升，但發病早期（12小時內）的闌尾炎指數本來就可能尚未衝高。"
        ],
        "critical_action": "住院醫師必須在活動中主動提出『不能出院』，並安排『複查理學檢查』或『做電腦斷層(CT)』，最後『照會小兒外科』。"
    }
}