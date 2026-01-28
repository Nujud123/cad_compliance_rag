# CAD Compliance Module — Integration Guide

This module provides the core logic for validating architectural room data (coming from CAD/CV pipelines) and attaching evidence from SBC documents using a lightweight RAG-style BM25 retrieval system.

It is intended to be used *inside the main backend* of the final project.  
This README explains **how to integrate it**, **how to call it**, and **what output structure the backend should expect**.

---

## 📁 Folder Overview

Inside the repo, the module lives here:

```
compliance_rag/
    analyze_plan.py      # Main entrypoint used by backend
    rule_engine.py       # Area/width/ventilation/unit rules
    rules_registry.py    # Definitions of all rules
    retrieval.py         # BM25 keyword retrieval + filtering
    text_picker.py       # Extracts short requirement-like sentences
    config.py            # Paths + constants

data/
    kb/
        kb_all_chunks.jsonl
        sbc1101_chunks.jsonl
        res_requirements_chunks.jsonl
        .built  # marker file indicating KB is ready
```

### Important:
- The backend **should NOT run OCR or KB-building scripts**.  
  These steps were already done, and the resulting JSONL knowledge base is included.
- The system only requires **data/kb/** to exist.

---

## 🚀 How to Use the Module in the Backend

You only need **one function**:

```python
from compliance_rag.analyze_plan import analyze_plan
```

### ✨ 1) Prepare the `rooms` data structure

Backend should send a list of rooms:

```python
rooms = [
    {
        "id": 1,
        "type": "Bedroom",
        "metrics": {
            "area_sqm": 12.5,
            "min_dimension_m": 3.0
        },
        "ventilation": {
            "has_window": True
        }
    },
    ...
]
```

### Minimum fields expected:
| Field | Description |
|-------|-------------|
| `id` | Room identifier |
| `type` | One of: Bedroom, Living, Kitchen, Bathroom, WC, Corridor, ServiceRoom, ExitDoor |
| `metrics.area_sqm` | Area in square meters |
| `metrics.min_dimension_m` | The minimum width/dimension |
| `ventilation.has_window` | Boolean |

The CV module of the main system should provide this structure.

---

## ✨ 2) Call `analyze_plan()`

```python
result = analyze_plan(
    project_id="some_id",
    asset_id="unit_01",
    rooms=rooms
)
```

---

## 📦 Output Format (for API/UI)

`result` is a dictionary structured like:

```json
{
  "project_id": "demo",
  "asset_id": "unit_01",
  "summary": {
    "rooms_total": 5,
    "violations_total": 3,
    "warnings_total": 1,
    "skipped_missing_data": 0
  },
  "violations": [
    {
      "rule_id": "SBC-TABLE-Bedroom-MIN-AREA",
      "room_id": 1,
      "room_type": "Bedroom",
      "expected": "area_sqm >= 6.5",
      "actual": "area_sqm = 5.0",
      "rule_sentence": "لا يقل الحد الأدنى لمساحة Bedroom عن 6.5 م².",
      "ref": {
        "doc": "RES_REQUIREMENTS",
        "section": "٤-١-٥ مساحات الغرف والفراغات السكنية:",
        "page": 12,
        "chunk_id": 51,
        "source": "RES_REQUIREMENTS_MISTRAL_OCR"
      }
    }
  ],
  "warnings": [...]
}
```

### Notes:
- `rule_sentence` is a short readable requirement extracted from the evidence text.
- `ref` contains the full citation needed for UI (document, page, section, chunk source).

---

## ⚙️ How the Backend Should Integrate This

### 1. Backend receives `rooms` (from CV module)
### 2. Backend calls `analyze_plan()`  
### 3. Backend sends output JSON directly to frontend.

No additional processing required.

---

## 🧪 Quick Test

Inside project root:

```bash
python - << "EOF"
from compliance_rag.analyze_plan import analyze_plan
rooms=[{"id":1,"type":"Bedroom","metrics":{"area_sqm":5,"min_dimension_m":2},"ventilation":{"has_window":False}}]
print(analyze_plan(project_id="demo", asset_id="unit", rooms=rooms))
EOF
```

---

## 🧩 Why This Module Is Easy to Integrate

- No model loading
- No GPU usage
- No external LLM calls
- Deterministic, fully offline
- Evidence retrieval is fast (BM25 over ~150–200 chunks)
- Output is unified and clean for UI

---

## 🔒 Backend Safety Checks

Before running evidence retrieval, backend *may* call:

```python
from compliance_rag import config
config.kb_ready()
```

If returns `False`, system still works (rules run normally), but evidence citations are skipped.

---

## ✔️ Done

