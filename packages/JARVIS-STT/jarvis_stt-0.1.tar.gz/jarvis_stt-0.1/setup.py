from setuptools import setup,find_packages

setup(
    name='JARVIS-STT',
    version='0.1',
    author='Genius',
    author_email='amarjeetshah93@gmail.com',
    description='This is speech to text package'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]