import os
import inspect
import importlib.metadata

def call_order():
    stack = inspect.stack()
    calls = []
    for s in reversed(stack):
        calls.append(s.filename)
    return calls

def caller_info():
    def _get_call_order(stack):
        counter = 0
        for s in reversed(stack):
            counter = counter + 1
            if ".py" in s.filename:
                return counter
        return 0

    stack = inspect.stack()
    parentframe = stack[len(stack) - _get_call_order(stack)][0]

    module_info = inspect.getmodule(parentframe)
    if module_info:
        mod = module_info.__name__.split('.')
        package = mod[0]
        module = mod[1]

    klass = None
    if 'self' in parentframe.f_locals:
        klass = parentframe.f_locals['self'].__class__.__name__

    caller = None
    if parentframe.f_code.co_name != '<module>':
        caller = parentframe.f_code.co_name

    line = parentframe.f_lineno

    return package, module, klass, caller, line

def get_distribution_name():
    package, module, klass, caller, line = caller_info()
    name = package
    return name

def get_distribution_files(name):
    files = []
    for f in importlib.metadata.files(name):
        path = str(f.locate())
        path = os.path.basename(path)
        files.append(path)
    return files

def get_distribution_filepaths(name):
    files = []
    for f in importlib.metadata.files(name):
        path = str(f.locate())
        files.append(path)
    return files

def get_distribution_version(name):
    version = importlib.metadata.version(name)
    return version

def distribution_install_editable(name):
    for f in importlib.metadata.files(name):
        path = str(f.locate())
        if 'site-packages' in path and '.pth' in path:
            return True