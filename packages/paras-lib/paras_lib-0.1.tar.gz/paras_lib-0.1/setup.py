from setuptools import setup, find_packages
setup(
    name='paras_lib',
    version='0.1',
    packages=find_packages(),
    description='A custom functions package for common operations',
    author='Paras Singh',
    author_email='paras.singh@shl.com',
    url='https://github.com/embivert/paras_lib',  # Update with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)