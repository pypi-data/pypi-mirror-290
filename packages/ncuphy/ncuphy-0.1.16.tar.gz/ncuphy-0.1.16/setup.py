from setuptools import setup, find_packages


setup(
    name='ncuphy',
    version='0.1.16',
    author='Kah Seng Phay',
    author_email='phay_ks@icloud.com',
    description='A Raspberry Pi Python project for educational use.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ncuphy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    install_requires=[
        'RPi.GPIO',
        'numpy',
        'smbus2',
    ],
)
