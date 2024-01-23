from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='text_bridge',
    description='Allows to use prompt templates with OpenAI API',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    author='Damian Czapiewski',
    author_email='damianczap@outlook.com',
    packages=['text_bridge'],
    version='1.0.0',
    python_requires='>=3.6',
    install_requires=required
)
