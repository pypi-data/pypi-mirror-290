import json
import logging
import time
from pathlib import Path

import click
from mbench import profiling
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown as RichMarkdown


class Markdown:
    """Stream formatted JSON-like text to the terminal with live updates."""
    
    def __init__(self, lines, mdargs=None, style="default", save=False):
        """Initialize the Markdown class.

        Usage:
            >>> from markdown_stream import Markdown
            >>> md = Markdown(lines=[{"key": "value"}], mdargs=None, style="default")
            >>> md.stream()
        """
        self.lines = lines
        self.printed = ""
        self.mdargs = mdargs or {
            "code_theme": "github-light",
            "inline_code_theme": "github-light",
            "style": style or "reverse",
        }
        self.style = self.mdargs.get("style", "reverse")
        self.console = Console(force_terminal=True, color_system="truecolor")
        self.live = Live(console=self.console, refresh_per_second=4)
        self.save = save


    def stream(self,depth=0):
        def generate_markdown(data, depth=depth):
            """Generate Markdown from JSON with headers based on depth."""
            markdown_lines = []
            indent = " " * (depth * 2)  # Indentation for nested structures
            
            if isinstance(data, dict):
                header_added = False
                for key, value in data.items():
                    # Add headers for the first level
                    if not header_added:
                        markdown_lines.append(f"{indent}### {data.get('name', 'Item')}\n")
                        header_added = True
                    markdown_lines.append(f"{indent}- **{key}**:")
                    if isinstance(value, dict | list):
                        markdown_lines.extend(generate_markdown(value, depth + 1))
                    else:
                        value_display = "None" if value is None else str(value)
                        markdown_lines.append(f"{indent}  - {value_display}")
            elif isinstance(data, list):
                for item in data:
                    markdown_lines.extend(generate_markdown(item, depth))
            else:
                markdown_lines.append(f"{indent}{data}")
            
            return markdown_lines

        # Check if the input is a string and attempt to parse it as JSON
        if isinstance(self.lines, str):
            try:
                self.lines = json.loads(self.lines)
            except json.JSONDecodeError:
                # If it's just a string, display as is
                self.lines = [self.lines]

        # Ensure we have a list of items to process
        if isinstance(self.lines, dict):
            self.lines = [self.lines]

        with self.live as live:
            self.printed = ""
            for line in self.lines:
                if line:
                    markdown_lines = generate_markdown(line)
                    for markdown_line in markdown_lines:
                        # Update line-by-line
                        self.printed += markdown_line + "\n"
                        live.update(RichMarkdown(self.printed.strip(), **self.mdargs))
                        time.sleep(0.1) 
                

@click.command("mdstream")
@click.argument("file")
@click.option("--save", is_flag=True, help="Save the output to a file.")
@click.option("include", "--include", "-i", multiple=True, help="Include specific file patterns.")
def cli(file, save, include = None):
    """Stream formatted JSON-like text or markdown files to the terminal with live updates.

    Usage:
        $ md-stream file.json
    """
    include = include or {".json", ".md", ".txt", ".yaml", ".toml", ".py"}
    logging.basicConfig(level=logging.INFO)
    def recursive_read(file):
        data = {}
        if Path(file).is_file() and Path(file).suffix in include and "__pycache__" not in str(file):
            logging.info(f"Reading file: {file}")
            with Path(file).open() as f:
                data[file] = f.read()
                return data
        if Path(file).is_dir():
            for file_path in Path(file).iterdir():
                data[file_path] = recursive_read(file_path)
            return data

        return {}
    
    md = Markdown(lines=recursive_read(file))
    md.stream()

def example():
    # Example usage with a nested dictionary
    nested_data = {
        "name": "Example Package",
        "version": "1.0.0",
        "description": "This is a deeply nested structure.",
        "dependencies": [
            {
                "name": "Dependency 1",
                "version": "2.0.0",
                "sub_dependencies": [
                    {
                        "name": "Sub-dependency A",
                        "version": "2.1.1",
                        "details": {
                            "maintainer": "John Doe",
                            "license": "MIT"
                        }
                    },
                    {
                        "name": "Sub-dependency B",
                        "version": "2.1.2",
                        "details": {
                            "maintainer": "Jane Smith",
                            "license": "Apache-2.0"
                        }
                    }
                ]
            },
            {
                "name": "Dependency 2",
                "version": "3.0.0",
                "sub_dependencies": [
                    {
                        "name": "Sub-dependency C",
                        "version": "3.1.0",
                        "details": {
                            "maintainer": "Alice Brown",
                            "license": "GPL-3.0"
                        }
                    }
                ]
            }
        ],
        "urls": {
            "Homepage": "https://example.com",
            "Repository": "https://github.com/example/package"
        }
    }

    md_nested = Markdown(lines=[nested_data])
    md_nested.stream()


if __name__ == "__main__":
    cli()