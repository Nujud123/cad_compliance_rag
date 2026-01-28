# config.py
from __future__ import annotations
from pathlib import Path

PROJECT_NAME = "CAD Compliance RAG"

# cad_compliance_rag/
ROOT_DIR = Path(__file__).resolve().parent.parent

# cad_compliance_rag/data/
DATA_DIR = ROOT_DIR / "data"
KB_DIR = DATA_DIR / "kb"
OCR_DIR = DATA_DIR / "ocr"

# JSONL knowledge base paths
KB_ALL_PATH = KB_DIR / "kb_all_chunks.jsonl"
KB_SBC1101_PATH = KB_DIR / "sbc1101_chunks.jsonl"
KB_RES_REQ_PATH = KB_DIR / "res_requirements_chunks.jsonl"

DEFAULT_TOP_K = 3
DEFAULT_MIN_SCORE = 0.1

def kb_ready() -> bool:
    """
    Returns True if the KB JSONL exists (built once).
    Runtime can still work without KB, but evidence retrieval will be skipped.
    """
    return (KB_DIR / ".built").exists() and KB_ALL_PATH.exists()

