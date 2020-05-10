import warnings
import inspect

class _Writer(object):
    '''Generic writer used to format content with consistent indentation.'''

    _INDENT = ' ' * 4
    # Note: This should match a single indent used in the actual source code,
    #       that way, if content written using this class includes indentation,
    #       the formatted output will have consistent indentation.

    def __init__(self, write_line):
        ''':param write_line: Function that writes a given string to a new line.'''

        self._indent_level = 0
        self._write_line = write_line

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
                self._write_line(self._INDENT * self._indent_level + line + '\n')
        else:
            self._write_line('\n')
          
        return self

class _FileWriter(_Writer):
    '''File writer used to format content with consistent indentation.'''

    def __init__(self, file):
        ''':param file: File to write to, as a file path.'''

        self._file = open(file, 'w')
        super(_FileWriter, self).__init__(self._file.write)

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

        self.close()

    def close(self):
        '''Close the file writer.'''

        self._file.close()

class _StringWriter(_Writer):
    '''String writer used to format content with consistent indentation.'''

    def __init__(self):
        self._lines = []
        super(_StringWriter, self).__init__(self._lines.append)

    def get(self):
        '''Get the formatted string.'''
        
        return ''.join(self._lines)
