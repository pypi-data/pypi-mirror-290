from setuptools import setup, find_packages

setup(
    name='easytailwind',
    version='0.1.0',  # Update this version as needed
    description='A utility to set up Tailwind CSS in a python project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sayed Afaq',
    author_email='chief.specteria@gmail.com',
    url='https://github.com/H-BlaZe/easytailwind',  # Update with your repository URL
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'easytailwind=easytailwind.easytailwind:install',  # Replace `your_script` with your script name
        ],
    },
    install_requires=[
        'colorama',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
