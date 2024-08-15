import os, sys, traceback
import subprocess
from petljapub.config import read_config
from . import logger

# we expect that all custom compilation scripts reside in the data directory of petljapub

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

def tgen_dir():
    return os.path.join(data_dir, "tgen")

def compile_c(src_file, exe_file):
    c_compiler = read_config("c_compiler")
    if not c_compiler:
        logger.error("C compiler is not configured. Ensure it is installed and configure it using 'petljapub configure'")
        return False
        
    flags = "-O2 -Wall -Wno-sign-compare"
    args = [src_file, "-o", exe_file] + flags.split()
    (status, p) = run_exe("gcc", args=args)
    return status == "OK" and p.returncode == 0

def compile_cpp(src_file, exe_file):
    cpp_compiler = read_config("cpp_compiler")
    if not cpp_compiler:
        logger.error("C++ compiler is not configured. Ensure it is installed and configure it using 'petljapub configure'")
        return False

    if cpp_compiler == "G++":
        flags = "-O2 -Wall -Wno-sign-compare -std=c++17"
        args = [src_file, "-o", exe_file] + flags.split() + ["-I", tgen_dir()]
        (status, p) = run_exe("g++", args=args)
        return status == "OK" and p.returncode == 0
    else:
        logger.error("Unkown C++ compiler", cpp_compiler)
        return False

def compile_cs(src_file, exe_file):
    cs_compiler = read_config("cs_compiler")
    if not cs_compiler:
        logger.error("C# compiler is not configured. Ensure it is installed and configure it using 'petljapub configure'")
        return False

    if cs_compiler == "MSVC#":
        flags = "-optimize"
        args = ["-out:{}".format(exe_file), src_file] + flags.split()
        (status, p) = run_exe("csc", args=args)
        return status == "OK" and p.returncode == 0
    elif cs_compiler == ".NET":
        # script for .net core compilation
        compiler_script = os.path.join(data_dir, "compile-cs.sh")
        cmd = ["\"{}\" \"{}\"".format(compiler_script, os.path.basename(src_file))]
        (status, p) = run_exe(cmd, shell=True)
        return status == "OK" and p.returncode == 0
    elif cs_compiler == "MONO":
        flags=""
        args = [src_file, "-out:{}".format(exe_file)] + flags.split()
        (status, p) = run_exe("mcs", args=args)
        return status == "OK" and p.returncode == 0
    else:
        logger.error("Unkown C# compiler", cs_compiler)
        return False

def run_latex(tex_file, no_latex_mk=False, quiet=False, timeout=None):
    latex = read_config("latex")
    if not latex:
        logger.error("LaTeX is not installed and configured. Cannot produce pdf.")
        return

    if not quiet:
        out_file = sys.stdout
    else:
        out_file = subprocess.DEVNULL

    latex_mk = read_config("latex_mk")
    if not no_latex_mk and latex_mk:
        return run_exe("latexmk", args=[os.path.basename(tex_file), "-xelatex"], out_file=out_file, timeout=timeout, cwd=os.path.dirname(os.path.abspath(tex_file)))
    else:
        if not no_latex_mk:
            logger.warn("No LaTeX make system found. Compiling only once.")
        return run_exe("xelatex", args=[os.path.basename(tex_file), "-interaction=nonstopmode"], out_file=out_file, timeout=timeout, cwd=os.path.dirname(tex_file))
    
def run_exe(exe_file, args=[], in_file=sys.stdin, out_file=sys.stdout, timeout=None, cwd=None, shell=False, check=True):
    try:
        p = subprocess.run([exe_file] + args, stdin=in_file, stdout=out_file, timeout=timeout, cwd=cwd, check=check)
    except subprocess.TimeoutExpired:
        return ("TLE", None)
    except subprocess.CalledProcessError as e:
        logger.warn(exe_file, "raised an exception", "return value", e.returncode, verbosity=3)
        return ("RTE", None)
    except:
        logger.warn(exe_file, "raised an exception", verbosity=3)
        return ("RTE", None)
    logger.info(exe_file, "completed successfully returning", p.returncode, verbosity=6)
    return ("OK", p)

    
def run_py(src_file, in_file=sys.stdin, out_file=sys.stdout, timeout=None, args=[], cwd=None):
    python = read_config("python")
    if not python:
        logger.error("python is not configured. Ensure it is installed and configure it using 'petljapub configure'")
        return False

    return run_exe(python, args=[src_file] + args, in_file=in_file, out_file=out_file, timeout=timeout, cwd=cwd)
