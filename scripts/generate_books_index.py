from pathlib import Path
from urllib.parse import quote

BOOKS_DIR = Path("books")
README = Path("README.md")

START = "<!-- BOOKS-LIST:START -->"
END = "<!-- BOOKS-LIST:END -->"

def clean_title(filename: str) -> str:
    title = Path(filename).stem
    title = title.replace("_", " ").replace("-", " ")
    return " ".join(title.split())

def main():
    pdfs = sorted(BOOKS_DIR.glob("*.pdf"), key=lambda p: p.name.lower())

    if not pdfs:
        generated = "_No PDF books uploaded yet._"
    else:
        lines = [
            "| Book | File |",
            "|---|---|",
        ]

        for pdf in pdfs:
            title = clean_title(pdf.name)
            encoded_path = quote(str(pdf).replace("\\", "/"))
            lines.append(f"| [{title}]({encoded_path}) | `{pdf.name}` |")

        generated = "\n".join(lines)

    readme_text = README.read_text(encoding="utf-8")

    if START not in readme_text or END not in readme_text:
        raise ValueError("README.md must contain BOOKS-LIST markers.")

    before = readme_text.split(START)[0]
    after = readme_text.split(END)[1]

    new_readme = f"{before}{START}\n{generated}\n{END}{after}"

    README.write_text(new_readme, encoding="utf-8")

if __name__ == "__main__":
    main()
