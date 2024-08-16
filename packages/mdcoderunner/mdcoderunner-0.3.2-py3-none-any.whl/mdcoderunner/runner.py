import math
from .imports import *
from .config import *
from .utils import get_hash, test_cache_hit

class Executer:
    def __init__(self):
        if not os.path.exists(TEMPFOLDER):
            os.mkdir(TEMPFOLDER)
    def remove_temp(self):
        for f in os.listdir(TEMPFOLDER):
            os.remove(os.path.join(TEMPFOLDER, f))
    def _prepare_script(self, file, language='cpp', input = None):
        if language == 'py':
            script = f"{PYTHON_LOCATION} {file}"
        elif language == 'cpp':
            temp = os.path.join(TEMPFOLDER, 'temp')
            script = f"{GPP_LOCATION} -o {temp} {file} && {temp}"
        elif language == 'c':
            temp = os.path.join(TEMPFOLDER, 'temp')
            script = f"{GPP_LOCATION} -x c -o {temp} {file} && {temp} "
        else:
            raise Exception("Language not supported")

        if input:
            in_file = os.path.join(TEMPFOLDER, 'input.text')
            with open(in_file, 'w') as f:
                f.write(input)
            script = f"{script} < {in_file}"
        return script
    
    # def _run_script(self, script):
    #     try:
    #         result = subprocess.run(script, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,timeout = TIMEOUT)
    #     except subprocess.CalledProcessError as e:
    #         result = e
    #     return result

    def _run_script(self, script):
        try:
            # Create a pipe for stdout and stderr
            stdout_pipe = subprocess.PIPE
            stderr_pipe = subprocess.PIPE

            # Using 'tee' to duplicate the output to both stdout/stderr and the PIPE
            command = f"({script}) 2>&1 | tee /dev/tty"  # 2>&1 redirects stderr to stdout
            process = subprocess.Popen(command, shell=True, stdout=stdout_pipe, stderr=stderr_pipe, stdin=None)

            stdout, stderr = process.communicate(timeout=TIMEOUT)

            # Return the result as if it were from `subprocess.run`
            return subprocess.CompletedProcess(
                args=script,
                returncode=process.returncode,
                stdout=stdout,
                stderr=stderr
            )
        except subprocess.CalledProcessError as e:
            return e
        except subprocess.TimeoutExpired as e:
            process.kill()
            return e

    def timeit(self, script, passthrough=False):
        times = []
        for _ in range(NRUNS_TIMEIT):
            tick = time.time() * 1000
            result = self._run_script(script)
            tock = time.time() * 1000
            times.append(tock-tick)
        mean_time = sum(times)/len(times)
        max_time = max(times)
        min_time = min(times)
        std_time = math.sqrt(sum([(t-mean_time)**2 for t in times])/len(times))
        return {
            'mean': round(mean_time,PRECISION),
            'max': round(max_time,PRECISION),
            'min': round(min_time,PRECISION),
            'std': round(std_time,PRECISION),
            'nruns': len(times)
        }

    def execute(self, file=None, code=None, language='cpp', input = None,timeit=False):
        if not file and not code:
            raise Exception("Either file or code must be provided")
        fileObj = None
        if code:
            file = os.path.join(TEMPFOLDER, f'temp.{language}')
            with open(file, 'w') as f:
                f.write(code)
        script = self._prepare_script(file, language, input)

        tick = time.time() * 1000
        result = self._run_script(script)
        tock = time.time() * 1000
        timetaken = tock-tick

        if timeit:
            timeit_result = self.timeit(script)

        if fileObj:
            fileObj.close()

        err = result.stderr.decode('utf-8')
        res = result.stdout.decode('utf-8')
        self.remove_temp()
        ret =  {
            'output': res or NOOUTPUT,
            'error': err or NOERR,
            'timetaken': round(timetaken,PRECISION),
            'nruns': timeit,
            'status': False if err else True
        }
        if timeit:
            ret['timeit'] = timeit_result
            ret['timetaken'] = timeit_result['mean']
        return ret
    def run_block(self,block,passthrough=False):
        output = []
        inputs = block['input']
        code = block['code']
        lang = block['lang']
        timeit = TIMEIT in block['attr']['class']
        if inputs:
            for inp in inputs:
                if not passthrough:
                    res = self.execute(code=code, language=lang, input=inp, timeit=timeit)
                else:
                    res = {}
                output.append({**res, 'input': inp})
        else:
            if not passthrough:
                res = self.execute(code=code, language=lang, timeit=timeit)
            else:
                res = {}
            output.append(res)
        block['output'] = output
        block['attr']['hash'] = get_hash(block)

        return block
    

if __name__ == "__main__":
    code = """\
#include <iostream>
using namespace std;
int main()
{
cout << "Hello, World!";
}
    """
    executer = Executer()
    output = executer.execute(code=code, language='cpp')

    for k, v in output.items():
        print(k, v)
        
        