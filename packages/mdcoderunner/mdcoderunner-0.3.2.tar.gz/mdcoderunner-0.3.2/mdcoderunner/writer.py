from .imports import *
from .config import *
from .config import config_dict

def generate_attrs(block):
    s = ''
    for k, v in block['attr'].items():
        if isinstance(v, list):
            v = ' '.join(set(v))
        s += f'{k}="{v}" '
    return s.strip()

template = jinja2.Template(TEMPLATE)

def render_block(block):
    block_md = template.render(attrs=generate_attrs(block), 
                    code=block['code'],
                    outputs=block['output'] if 'output' in block else [],
                    status_color='green',
                    lang=block['lang'],
                    config=config_dict).replace(TTRICKS,'```')

    return block_md

def render_blocks(blocks):
    blocks = [{**block, 'rendered': render_block(block)} for block in blocks]

    return blocks

if __name__ == "__main__":
    example = [
        {
            "raw": "<codeStart/>\n```python\nprint(\"Hello, World!\")\n```\n<codeEnd/>",
            "attr": {},
            "content": "\n```python\nprint(\"Hello, World!\")\n```\n",
            "input": [],
            "code": "print(\"Hello, World!\")",
            "lang": "py"
        }
    ]

    blocks = render_blocks(example)
    print(blocks)