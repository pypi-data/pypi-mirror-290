from mistletoe import markdown as render_markdown
from pathlib import Path
from shutil import rmtree

def main():
    print(" - Erasing output/ directory")
    try:
        rmtree("output")
    except FileNotFoundError:
        pass

    template_path = Path(__file__).parent / "template.html"

    with template_path.open("r") as template_file:
        template = template_file.read()

    for input_path in Path("input").rglob("*.md"):
        with input_path.open("r") as input_file:
            # Load up the Markdown
            markdown = input_file.read()

            # Render the content
            html_content = render_markdown(markdown)

            # Extract the Heading 1
            for line in markdown.split("\n"):
                if line.startswith("# "):
                    title = line[2:]
                    break
            else:
                print(f"{input_path} is missing Heading 1")
                return 1

            # Generate the output
            html_output = template.replace("TITLE", title).replace("CONTENT", html_content)

            # Get the output path
            output_path = Path(str(input_path).replace("input", "output", 1)[:-2]+"html")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to disk
            with output_path.open("w") as output_file:
                output_file.write(html_output)

            # Print status
            print(f" - Converted {input_path} to {output_path}")
    return 0
