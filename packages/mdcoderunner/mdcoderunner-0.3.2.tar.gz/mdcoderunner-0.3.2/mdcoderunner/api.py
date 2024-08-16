import argparse
from .imports import *
from .config import *
from .utils import remove_excess_newlines
from . import MarkdownParser, render_blocks, Executer

class API:
    def __init__(self):
        self.parser = MarkdownParser(EQUIVALENCE, SUPPORTED_LANGUAGES, DIV_REGEX, ATTR_REGEX, CODE_REGEX)
        self.executor = Executer()
    
    def pipeline(self, markdown_code):
        parsed = self.parser.parse(markdown_code)
        executed = [self.executor.run_block(block) for block in parsed]
        rendered = render_blocks(executed)
        for block in rendered:
            markdown_code = markdown_code.replace(block['raw'], block['rendered'])
        return markdown_code
    
    def read(self, path):
        with open(path, 'r') as f:
            markdown_code = f.read()
        return markdown_code
    
    def write(self, path, markdown_code):
        with open(path, 'w') as f:
            f.write(markdown_code)

    def clear_outputs(self, markdown_code):
        parsed = self.parser.parse(markdown_code)
        executed = [self.executor.run_block(block, passthrough=True) for block in parsed]
        cleared = render_blocks(executed)
        for block in cleared:
            markdown_code = markdown_code.replace(block['raw'], block['rendered'])
        markdown_code = re.sub(r'(hash="\w*?")/>','/>',markdown_code) # remove hash
        return markdown_code
    
    def create_code_tags(self, markdown_code):
        for lang in SUPPORTED_LANGUAGES:
            pattern = re.compile(rf'(```{re.escape(lang)}\n.*?\n```)', re.DOTALL)
            markdown_code = pattern.sub(r'<codeStart/>\n\n\1\n\n<codeEnd/>', markdown_code)
        return markdown_code
    
    def clear_code_tags(self, markdown_code):
        markdown_code = markdown_code.replace('<codeStart/>', '')\
                                    .replace('<codeEnd/>', '')
        return markdown_code

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process a Markdown file with executable code blocks.")
    parser.add_argument("input_path", type=str, help="Path to the input Markdown file.")
    parser.add_argument("output_path", type=str, nargs="?", help="Path to the output Markdown file (optional). If not provided, the input file will be overwritten.")
    parser.add_argument("--clear-outputs", action="store_true", help="Clear all code outputs in the Markdown file.")
    parser.add_argument("--create-code-tags", action="store_true", help="Wrap code blocks in <codeStart/> and <codeEnd/> tags.")
    parser.add_argument("--clear-code-tags", action="store_true", help="Remove <codeStart/> and <codeEnd/> tags from code blocks.")

    # Parse the arguments
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path or input_path  # Use the input path if output path is not provided

    # Create an instance of the API
    api = API()

    # Read the input file
    markdown_code = api.read(input_path)

    # Apply the requested processing
    if args.clear_outputs:
        markdown_code = api.clear_outputs(markdown_code)
    if args.create_code_tags:
        markdown_code = api.create_code_tags(markdown_code)
    if args.clear_code_tags:
        markdown_code = api.clear_code_tags(markdown_code)
    
    # Process the markdown file if no special options are provided
    if not args.clear_outputs and not args.create_code_tags and not args.clear_code_tags:
        markdown_code = api.pipeline(markdown_code)

    # Remove excess newlines
    markdown_code = remove_excess_newlines(markdown_code)

    # Write the output file
    api.write(output_path, markdown_code)

    print(f"Processed markdown file saved to {output_path}")

if __name__ == "__main__":
    main()