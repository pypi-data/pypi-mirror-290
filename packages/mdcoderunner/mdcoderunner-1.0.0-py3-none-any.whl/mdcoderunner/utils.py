from .imports import *
import shutil

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



def check_bash_availability():
    bash_path = shutil.which("bash")
    if bash_path:
        return True
    else:
        print("Bash is not available on this system. Using default!")
        return False