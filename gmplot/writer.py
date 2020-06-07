import warnings
import inspect
from .utility import _INDENT

class _Writer(object):
    '''Writer used to format content with consistent indentation.'''

    def __init__(self, file):
        ''':param file: File to write to.'''

        self._file = file
        self._indent_level = 0

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''
        :param exception_type: Type of exception that triggered the exit. 
        :param exception_value: Value of exception that triggered the exit.
        :param traceback: Traceback when exit was triggered.
        '''

        # Clear the file if an uncaught exception occured while writing:
        if exception_type:
            self._file.truncate(0)

    def indent(self):
        '''Indent the writer by one level.'''

        self._indent_level += 1
        return self

    def dedent(self):
        '''Dedent the writer by one level.'''

        if self._indent_level > 0:
            self._indent_level -= 1
        else:
            warnings.warn("Can't dedent further!")
            
        return self

    def write(self, content=''):
        '''
        Write content.

        :param content: (optional) Content to write, as a string. If empty, a new line is written.
            Content is cleaned using the same rules as Python's `inspect.cleandoc()`:
            - Leading and trailing empty lines are removed.
            - Any leading whitespace common to all lines is removed.
            - All tabs are expanded to spaces.
        '''

        lines = inspect.cleandoc(content).splitlines()

        if lines:
            for line in lines:
                self._file.write(_INDENT * self._indent_level + line + '\n')
        else:
            self._file.write('\n')
          
        return self
