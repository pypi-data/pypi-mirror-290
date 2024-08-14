from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="grep_excel",
    version="1.0.0",
    description="A grep-like utility for searching Excel files",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/stenzr/grep_excel",
    author="Rohit Kumar",
    author_email="rkrohitkr01@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'grep_excel=grep_excel.cli:main',
        ],
    },
    install_requires=install_requires,
    python_requires='>=3.6',
    extras_require={
        'test': ['unittest', 'coverage'],
    },
)
