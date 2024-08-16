import re
from .config import *
from .utils import get_hash, test_cache_hit

class MarkdownParser:
    def __init__(self, equivalence, supported_languages, div_regex, attr_regex, code_regex):
        self.EQUIVALENCE = equivalence
        self.SUPPORTED_LANGUAGES = supported_languages
        self.INV_EQUIVALENCE = {}
        self.div_regex = re.compile(div_regex, re.DOTALL)
        self.attr_regex = re.compile(attr_regex, re.DOTALL)
        self.code_pattern = re.compile(code_regex, re.DOTALL)

        self.prepare_equivalence()

    def prepare_equivalence(self):
        """Prepare the equivalence mappings and supported languages."""
        for k, v in self.EQUIVALENCE.items():
            if k not in self.SUPPORTED_LANGUAGES:
                self.SUPPORTED_LANGUAGES.append(k)
            for lang in v:
                if lang not in self.SUPPORTED_LANGUAGES:
                    self.SUPPORTED_LANGUAGES.append(lang)

            self.INV_EQUIVALENCE.update({lang: k for lang in v})

        for lang in self.SUPPORTED_LANGUAGES:
            if lang not in self.INV_EQUIVALENCE:
                self.INV_EQUIVALENCE[lang] = lang

    def parse(self, markdown_code):
        """Parse the given markdown code and return the structured data."""
        parsed = []
        for raw, attr, content in self.div_regex.findall(markdown_code):
            attr = dict(re.findall(self.attr_regex, attr))
            if 'class' in attr:
                attr['class'] = attr['class'].split(' ')
            else:
                attr['class'] = []
            parsed.append({
                'raw': raw,
                'attr': attr,
                'content': content
            })
        
        for block in parsed:
            block['input'] = []
            block['code'] = None
            for raw, lang, content in self.code_pattern.findall(block['content']):
                if lang in self.SUPPORTED_LANGUAGES:
                    assert block['code'] is None, 'Multiple code blocks found!'
                    block['code'] = content
                    block['lang'] = self.INV_EQUIVALENCE[lang]
                if lang == 'input':
                    block['input'].append(content)
                if lang == 'output':
                    block['output'] = content
        
        # Remove blocks that are marked with the SKIP class
        parsed = [block for block in parsed if not SKIP in block['attr']['class']]
        for block in parsed:
            if TIMEIT in block['attr']['class']:
                block['attr']['class'].append(NOCACHE)
        
        # Use cached previous results if possible
        out = []
        for block in parsed:
            if (NOCACHE in block['attr']['class']):
                out.append(block)
            else:
                if test_cache_hit(block):
                    pass # cache hit, skip it
                else:
                    out.append(block)

        return out

# Example usage:
if __name__ == "__main__":
    from config import *
    import json

    # Initialize the parser with the required configurations
    parser = MarkdownParser(EQUIVALENCE, SUPPORTED_LANGUAGES, DIV_REGEX, ATTR_REGEX, CODE_REGEX)

    # Example markdown content to parse
    markdown_content = """
<codeStart/>
```python
print("Hello, World!")
```
<codeEnd/>"""

    # Parse the markdown content
    parsed_output = parser.parse(markdown_content)

    # Display the parsed output
    for block in parsed_output:
        print('==' * 20)
        for key, value in block.items():
            print(key)
            print(value)
            print('--' * 20)

    print(json.dumps(parsed_output, indent=4))