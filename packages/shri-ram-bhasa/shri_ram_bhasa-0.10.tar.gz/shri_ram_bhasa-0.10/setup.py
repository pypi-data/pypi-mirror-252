from setuptools import setup, find_packages

setup(
    name='shri_ram_bhasa',  
    version='0.10',  
    description='ram programing language',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/viveakrt/ram.git',
    author='Vivek', 
    author_email='carbonvivek@gmail.com', 
    packages=find_packages(),  
    classifiers=[  
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',  
    entry_points={  
        'console_scripts': [
            'ram=shri_ram_bhasa.ramji:main',
        ],
    },
)
