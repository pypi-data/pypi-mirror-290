from setuptools import setup, find_packages

setup(
    name="woe-credit-scoring",  
    version="1.0.0",  
    description="Tools for creating credit scoring models",  
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    author="José Fuentes",
    author_email="jose.gustavo.fuentes@gmail.com",
    url="https://github.com/JGFuentesC/woe_credit_scoring", 
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=["scikit-learn>=1.3.2",
                      "pandas>=1.5.3",
                      "numpy>=1.24.4",
                      "matplotlib>=3.8.4",
                      "seaborn==0.13.2"
                      ],
)
