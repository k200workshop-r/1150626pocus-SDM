#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patient Case Profile: Pancreatic Adenocarcinoma with Obstructive Jaundice
Source Medical Records Date Range: 2026-05-15 to 2026-05-25
"""

patient_case = {
    # =========================================================================
    # 1. 基本資料 (Demographics & History)
    # =========================================================================
    "demographics": {
        "age": 52,
        "gender": "Male",
        "past_medical_history": [
            "Diabetes mellitus (DM)",
            "Hepatitis B carrier"
        ]
    },

    # =========================================================================
    # 2. 入院紀錄 (Admission Note)
    # =========================================================================
    "admission_note": {
        "date": "2026-05-15 18:01",
        "chief_complaint": "Jaundice and tea-colored urine since 7 days ago.",
        "present_illness": (
            "A 52-year-old male with DM and Hep B history presented with jaundice "
            "and tea-colored urine for 7 days. Associated with abdominal fullness, flatus, "
            "and weight loss of 2-3 kg/month. Denied fever, chills, chest pain, or GI symptoms. "
            "Local clinic suspected acute hepatitis due to abnormal LFTs. Symptoms worsened "
            "leading to GI outpatient referral and subsequent ED admission."
        ),
        "physical_examination": {
            "consciousness": "E4V5M6",
            "vital_signs": {
                "temperature_c": 36.5,
                "blood_pressure": "177/98 mmHg",
                "pulse_bpm": 80,
                "respiratory_rate_min": 18,
                "spo2_percent": 100  # Room air
            },
            "findings": [
                "Icteric sclera", 
                "Flat and non-tender abdomen", 
                "Freely movable extremities"
            ]
        },
        "laboratory_results": {
            "liver_function": {
                "GOT_U_L": 172,
                "GPT_U_L": 294,
                "r_GT_U_L": 1356
            },
            "bilirubin": {
                "total_mg_dl": 9.5,
                "direct_mg_dl": 9.3
            },
            "metabolic_renal": {
                "blood_glucose_mg_dl": 161,
                "creatinine_mg_dl": 1.3
            }
        },
        "imaging_findings": {
            "chest_xray_20260515": [
                "Mildly exaggerated lung markings over both lower lung zones",
                "Bilateral costophrenic angles are sharp",
                "Cardiac size and mediastinal width within normal limits",
                "Thoracic vertebrae: mild scoliosis"
            ],
            "upper_abdomen_ct_20260515": {
                "findings": [
                    "Suspicious ill-defined hypoenhancing nodular lesion at the uncinate process and head of the pancreas accompanied by dilatation of the main pancreatic duct and mild dilatation of bilateral intrahepatic ducts and common bile duct.",
                    "Tiny cyst at the right kidney.",
                    "Enlargement with calcification of the prostate gland.",
                    "Arteriosclerotic changes with mural calcifications of the aorta and bilateral iliac arteries.",
                    "Degenerative spondylosis with marginal spur over the lumbar spine."
                ],
                "impression": [
                    "Suspicious pancreatic uncinate process and head ill-defined hypoenhancing nodular lesion with upstream PD dilatation, bilateral IHDs and CBD mild dilatation; dddx includes pancreatic head tumor such as malignancy.",
                    "Tiny right renal cyst.",
                    "Prostatic enlargement with calcification."
                ]
            }
        },
        "initial_impression": [
            "Obstructive jaundice",
            "Suspected pancreatic head tumor"
        ]
    },

    # =========================================================================
    # 3. 病程紀錄 (Progress Notes)
    # =========================================================================
    "progress_notes": {
        "date_range": "2026-05-18 to 2026-05-25",
        "subjective_20260518": [
            "No fever",
            "No abdominal pain",
            "Tolerated endoscopic retrograde cholangiopancreatography (ERCP) examination and treatment"
        ],
        "vitals_20260518": [
            {"time": "09:00", "BT_C": 36.7, "RR_min": 18, "PR_bpm": 69, "BP": "161/81", "SpO2": 99, "pain_score": 1},
            {"time": "15:25", "BT_C": 35.4, "RR_min": 18, "PR_bpm": 72, "BP": "126/77", "SpO2": 99, "pain_score": None},
            {"time": "16:25", "BT_C": 36.2, "RR_min": 18, "PR_bpm": 69, "BP": "153/82", "SpO2": 100, "pain_score": None},
            {"time": "16:50", "BT_C": 36.4, "RR_min": 18, "PR_bpm": 69, "BP": "164/80", "SpO2": 98, "pain_score": 0}
        ],
        "io_20260518": {
            "input_ml": 0,
            "output_ml": 380
        },
        "blood_sugar_20260518": [
            {"time": "05:38", "value_mg_dl": 144},
            {"time": "15:33", "value_mg_dl": 122}
        ],
        "ercp_report_20260518": {
            "procedure": "Endoscopic Sphincterotomy (經內視鏡括約肌切開術)",
            "icd_codes": {
                "primary": "R17 Unspecified jaundice", 
                "secondary": "R94.5 Abnormal results of LFTs"
            },
            "findings": (
                "Duodenoscope inserted to 2nd portion. Normal ampulla of Vater. 5mm 0-Is polyp at posterior wall of high body. "
                "Pancreatic duct cannulated twice, transpancreatic sphincterotomy done, single pigtail plastic stent (Advanix 5Fr x 5cm) placed to MPD. "
                "CBD successfully cannulated; Cholangiogram showed normal caliber of IHDs/CBD with smooth tapering at distal CBD, gallstones and PTCD. "
                "Further endoscopic sphincterotomy and endobiliary biopsy x3 done at distal CBD. Plastic stent (Advanix 8.5Fr x 7cm) deployed through CBD."
            ),
            "impression": [
                "Distal CBD tapering, r/o external compression",
                "Status post transpancreatic sphincterotomy and papillotomy",
                "Status post endobiliary biopsy, ERBD, and ERPD",
                "Gallstones",
                "Gastric polyp"
            ],
            "complications": "Nil"
        },
        "medications": {
            "antibiotics": "Flomoxef Na 1000 mg Q8H IVD (2026-05-15 16:05 to 2026-05-22 16:05)"
        }
    },

    # =========================================================================
    # 4. 出院紀錄 (Discharge Note)
    # =========================================================================
    "discharge_note": {
        "date": "2026-05-25 11:36",
        "discharge_diagnosis": [
            "Pancreas adenocarcinoma, with multiple hepatic metastasis (confirmed by ERCP biopsy on 05/18 and Pancreas MRI on 05/23)",
            "Obstructive jaundice"
        ],
        "hospital_course": [
            "2026-05-15: Admitted via ED due to obstructive jaundice; CT noted suspicious pancreatic head tumor.",
            "2026-05-16: Arranged PTCD for urgent jaundice relief.",
            "2026-05-18: Performed ERCP for jaundice/cholangitis relief, ERBD stent placed, endobiliary biopsy performed.",
            "2026-05-20: Chest CT performed, negative for lung metastasis.",
            "2026-05-21: Pathology report from ERCP confirmed Adenocarcinoma.",
            "2026-05-22: General Surgery (GS) and Oncology consultations completed for tumor evaluation.",
            "2026-05-23: Pancreas MRI confirmed uncinate process malignancy with distal pancreatic ductal dilatation & multiple hepatic metastases.",
            "Post-MRI: Condition explained to patient. Patient decided to seek a second opinion at National Taiwan University Hospital (NTUH) and requested Against Advice Discharge (AAD)."
        ],
        "discharge_medication": "Nil",
        "instructions": "Against Advice Discharge (AAD). Transfer to National Taiwan University Hospital (台大醫院) for further medical opinion and treatment."
    }
}

# =============================================================================
# 簡單測試：列印出院診斷與後續處置
# =============================================================================
if __name__ == "__main__":
    print("=== 病歷資料讀取成功 ===")
    print(f"病患診斷: {patient_case['discharge_note']['discharge_diagnosis'][0]}")
    print(f"出院醫囑: {patient_case['discharge_note']['instructions']}")