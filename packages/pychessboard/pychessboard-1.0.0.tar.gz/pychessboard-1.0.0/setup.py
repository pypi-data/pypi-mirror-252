from setuptools import setup, find_packages

setup(
    name='pychessboard',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pygame'
    ],
    author='James gonzalez',
    author_email='jame-gonzalez.email@example.com',
    description='a chessboard game',
    long_description=open('README').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-package-name',
)
