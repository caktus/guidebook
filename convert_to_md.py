from pathlib import Path
import pandoc

docs_folder = Path("./docs")

def convert_to_md():
    for file in Path('./source').glob('**/*.rst'):
        parent_dir = file.parent
        # something with pandoc
        in_doc = pandoc.read(file=file.open(), format="rst")
        print(f"Reading: {file}")
        out_doc = pandoc.write(in_doc, format="markdown")

        out_dir = docs_folder / parent_dir.name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{file.stem}.md"
        print(f"Writing: {out_file}")
        out_file.write_text(out_doc)


if __name__ == "__main__":
    convert_to_md()