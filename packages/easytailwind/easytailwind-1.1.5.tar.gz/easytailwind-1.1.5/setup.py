from setuptools import setup, find_packages

setup(
    name='easytailwind',
    version='1.1.5',  # Update this version as needed
    description='A utility to set up Tailwind CSS in a python project.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sayed Afaq',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts":[
            "easytailwind = easytailwind:install",
            "easytailwind-v = easytailwind:check_et"
        ]
    }
)
