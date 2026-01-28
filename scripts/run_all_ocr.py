# scripts/run_all_ocr.py
from compliance_rag import config
from scripts.ocr_mistral import run_ocr


def main() -> None:
    run_ocr(
        pdf_path=str(config.DATA_DIR / "pdf" / "sbc1101.pdf"),
        out_md=str(config.OCR_DIR / "sbc1101_ocr.md"),
    )

    run_ocr(
        pdf_path=str(config.DATA_DIR / "pdf" / "اشتراطات إنشاء المباني السكنية.pdf"),
        out_md=str(config.OCR_DIR / "res_requirements_ocr.md"),
    )


if __name__ == "__main__":
    main()
