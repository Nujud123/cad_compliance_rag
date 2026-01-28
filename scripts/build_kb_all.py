# scripts/build_kb_all.py
from pathlib import Path
from compliance_rag import config
from scripts.kb_build_from_md import build_kb_from_md


def _concat_jsonl(out_path: Path, inputs: list[Path]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as w:
        for p in inputs:
            with p.open("r", encoding="utf-8") as r:
                for line in r:
                    if line.strip():
                        w.write(line)


def main() -> None:
    # ensure dirs exist
    config.OCR_DIR.mkdir(parents=True, exist_ok=True)
    config.KB_DIR.mkdir(parents=True, exist_ok=True)

    out1 = config.KB_DIR / "sbc1101_chunks.jsonl"
    out2 = config.KB_DIR / "res_requirements_chunks.jsonl"
    out_all = config.KB_DIR / "kb_all_chunks.jsonl"

    build_kb_from_md(
        md_path=config.OCR_DIR / "sbc1101_ocr.md",
        out_jsonl_path=out1,
        doc_id="SBC1101",
        source="SBC1101_MISTRAL_OCR",
    )

    build_kb_from_md(
        md_path=config.OCR_DIR / "res_requirements_ocr.md",
        out_jsonl_path=out2,
        doc_id="RES_REQUIREMENTS",
        source="RES_REQUIREMENTS_MISTRAL_OCR",
    )

    _concat_jsonl(out_all, [out1, out2])

    assert out_all.exists() and out_all.stat().st_size > 0
    # marker file (only if everything above succeeded)
    (config.KB_DIR / ".built").write_text("ok", encoding="utf-8")


if __name__ == "__main__":
    main()
