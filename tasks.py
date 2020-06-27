from invoke import task

@task
def test(c, report=False):
    c.run('coverage run -m unittest discover -v')
    c.run('coverage report' if report else 'coverage html')
