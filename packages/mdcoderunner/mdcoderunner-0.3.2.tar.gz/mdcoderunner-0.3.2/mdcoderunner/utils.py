from .imports import *

def get_hash(block):
    text = block['code'] + ' '.join(block['input'])
    hashcode= hashlib.sha256(text.encode()).hexdigest()
    return hashcode

def test_cache_hit(block):
    if not 'output' in block:
        return False
    if not 'hash' in block:
        return False
    
    if 'input' in block:
        o_inputs = [o['input'] for o in block['output']]
        if o_inputs != block['input']:
            return False
    
    return get_hash(block) == block['attr']['hash']

def remove_excess_newlines(text):
    return re.sub(r'\n{3,}', '\n\n', text)