# General
TIMEOUT = 5
PRECISION = 5
TEMPFOLDER = '/tmp/mdcoderunner'
NOERR = 'No Error'
NOOUTPUT = 'No Output'

SKIP = 'skip'
TIMEIT = 'timeit'
NOCACHE = 'nocache'

# Parsing
DIV_REGEX = r'(<codeStart(.*?)/>(.*?)<codeEnd/>)'
ATTR_REGEX = r'(\w+)\s*=\s*"(.*?)"'
CODE_REGEX = rf'(```(\w*?)\s*\n([\s\w\W]*?)\n```)'

# Runner
NRUNS_TIMEIT = 10
SUPPORTED_LANGUAGES = ['c', 'cpp', 'py']
EQUIVALENCE = {'py': ['python'], 'cpp': ['c++']}
PYTHON_LOCATION = "python3" # change this to your python location if needed
GPP_LOCATION = "g++" # change this to your g++ location if needed

# Writer
TTRICKS = "<!-- ``` -->" # avoid jinja errors, will be replaced by ```


TEMPLATE = """\
<codeStart {{attrs}}/>

<!-- ``` -->{{lang}}
{{code}}
<!-- ``` -->            

{% for output in outputs %}
{% if 'input' in output %}
<span style="color: #007ACC; font-weight: bold;">[INPUT]:</span>
<!-- ``` -->input                   
{{output.input}}
<!-- ``` -->
{% endif %}
{% if 'output' in output %}
<span style="color: {% if output.status %} #28A745{% else %}#D73A49{% endif %}; font-weight: bold;">[OUTPUT]:</span> <span style="font-size: small; color: #6A737D;">Time taken (ms): {{output.timetaken}}
</span>
<!-- ``` -->output                    
{{ output.output }}
<!-- ``` -->
{% endif %}
{% if 'error' in output %}
{% if output.error != config.NOERR %}
<span style="color: {% if output.status %} #28A745{% else %}#D73A49{% endif %}; font-weight: bold;">[ERROR]:</span>
</span>
<!-- ``` -->error                    
{{ output.error }}
<!-- ``` -->
{% endif %}
{% endif %}
{% if 'timeit' in output %}
<span style="color: {% if output.status %} #28A745{% else %}#D73A49{% endif %}; font-weight: bold;">[TIMEIT-RESULTS (ms)]:</span>
<!-- ``` -->timeit
mean: {{output.timeit.mean or 'undefined'}} +/- {{2 *output.timeit.std or 'undefined'}}
std: {{output.timeit.std or 'undefined'}}
max: {{output.timeit.max or 'undefined'}}
min: {{output.timeit.min or 'undefined'}}
with a total of {{output.timeit.nruns or 'undefined'}} runs
<!-- ``` -->
{% endif %}
{% endfor %}
                           
<codeEnd/>
"""



config_dict = {k: v for k, v in locals().items() if not k.startswith("__")}
