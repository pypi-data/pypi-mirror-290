from setuptools import setup, find_packages

setup(
    name='randomDateGenerator',  # Your project name
    version='0.1.0',
    description='A simple generator of random dates',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kaMod4/randomDateGenerator',  # Replace with your GitHub URL
    author='Ivan Miskinn',
    author_email='niksim.ytube@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
