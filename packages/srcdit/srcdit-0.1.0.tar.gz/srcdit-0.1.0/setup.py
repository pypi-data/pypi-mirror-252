from setuptools import setup, find_packages

setup(
    name='srcdit',
    version='0.1.0',
    author='Arpit Jain',
    description='Edit dotfiles from terminal',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)