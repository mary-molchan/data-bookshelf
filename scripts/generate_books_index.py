from pathlib import Path
from urllib.parse import quote

BOOKS_DIR = Path("books")
README = Path("README.md")

START = "<!-- BOOKS-LIST:START -->"
END = "<!-- BOOKS-LIST:END -->"


def clean_title(filename: str) -> str:
    """
    Converts a PDF filename into a cleaner display title.

    Example:
    "Algorithms_Illuminated_1_TIM_ROUGHGARDEN.pdf"
    becomes:
    "Algorithms Illuminated 1 TIM ROUGHGARDEN"
    """
    title = Path(filename).stem
    title = title.replace("_", " ").replace("-", " ")
    title = " ".join(title.split())
    return title


def format_size(size_bytes: int) -> str:
    """
    Converts file size from bytes to a readable format.
    """
    size_mb = size_bytes / (1024 * 1024)

    if size_mb >= 1:
        return f"{size_mb:.1f} MB"

    size_kb = size_bytes / 1024
    return f"{size_kb:.0f} KB"


def generate_books_table() -> str:
    """
    Generates a Markdown table with all PDF files from the books folder.
    """
    if not BOOKS_DIR.exists():
        return (
            "> [!WARNING]\n"
            "> The `books/` folder does not exist yet.\n\n"
            "_No PDF books uploaded yet._"
        )

    pdfs = sorted(
        BOOKS_DIR.glob("*.pdf"),
        key=lambda p: p.name.lower()
    )

    if not pdfs:
        return (
            "> [!NOTE]\n"
            "> No PDF books uploaded yet.\n\n"
            "_Add PDF files to the `books/` folder to generate the index automatically._"
        )

    lines = [
        f"**📚 Total books:** `{len(pdfs)}`",
        "",
        "> [!NOTE]",
        "> This index is generated automatically from PDF files stored in the `books/` folder.",
        "",
        "| 📚 Book | 📄 File | 💾 Size |",
        "| :--- | :--- | ---: |",
    ]

    for pdf in pdfs:
        title = clean_title(pdf.name)

        # Keeps links safe even when filenames contain spaces or special characters
        relative_path = str(pdf).replace("\\", "/")
        encoded_path = quote(relative_path, safe="/")

        file_size = format_size(pdf.stat().st_size)

        lines.append(
            f"| 📘 [{title}]({encoded_path}) | 📄 `{pdf.name}` | `{file_size}` |"
        )

    return "\n".join(lines)


def update_readme(generated_content: str) -> None:
    """
    Replaces the content between BOOKS-LIST markers in README.md.
    """
    if not README.exists():
        raise FileNotFoundError("README.md not found.")

    readme_text = README.read_text(encoding="utf-8")

    if START not in readme_text or END not in readme_text:
        raise ValueError(
            "README.md must contain the following markers:\n"
            f"{START}\n"
            f"{END}"
        )

    before = readme_text.split(START)[0]
    after = readme_text.split(END)[1]

    new_readme = f"{before}{START}\n{generated_content}\n{END}{after}"

    README.write_text(new_readme, encoding="utf-8")


def main() -> None:
    generated_content = generate_books_table()
    update_readme(generated_content)


if __name__ == "__main__":
    main()
