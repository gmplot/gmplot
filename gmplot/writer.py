import warnings
import inspect

class _FileWriter(object):
    '''
    File writer used to keep formatting consistent when writing content to a file.
    '''

    def __init__(self, file, **kwargs):
        '''
        :param file: File to write to, as a file path.
        :param indent: (optional) String to use as the indent.
        '''

        self._file = open(file, 'w')
        self._indent = kwargs.get('indent', ' ' * 4)
        self._indent_level = 0

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
         # Clear the file if an uncaught exception occured while writing:
        if exception_type:
            self._file.truncate(0)

        self.close()

    def write(self, content=''):
        '''
        Write content.

        :param content: (optional) String to write, cleaned up using the same
            rules as Python's `inspect.cleandoc()`. If empty, a new line is written.
        '''

        lines = inspect.cleandoc(content).splitlines()

        if lines:
            for line in lines:
                self._file.write(self._indent * self._indent_level + line + '\n')
        else:
            self._file.write('\n')
          
        return self

    def indent(self):
        '''
        Indent the writer by one level.
        '''

        self._indent_level += 1
        return self

    def dedent(self):
        '''
        Dedent the writer by one level.
        '''

        if self._indent_level > 0:
            self._indent_level -= 1
        else:
            warnings.warn("Can't dedent further!")
            
        return self

    def close(self):
        '''
        Close the file writer.
        '''

        self._file.close()
