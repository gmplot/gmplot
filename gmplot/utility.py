import sys

if sys.version_info.major == 2:
    from StringIO import StringIO as _StringIO

    class StringIO(_StringIO):
        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            '''
            :param exception_type: Type of exception that triggered the exit. 
            :param exception_value: Value of exception that triggered the exit.
            :param traceback: Traceback when exit was triggered.
            '''
            self.close()

else:
    from io import StringIO # pragma: no coverage
