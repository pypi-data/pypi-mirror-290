from setuptools import setup, find_packages

setup(
    name='dcen',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    description='Embed and retrieve hidden data using pixelated color codes in PNG files.',
    author='cdnserver',
    author_email='Xest03KmKtZUSETi@hidemail.app',
    url='https://github.com/cdnserver/DCEN',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
