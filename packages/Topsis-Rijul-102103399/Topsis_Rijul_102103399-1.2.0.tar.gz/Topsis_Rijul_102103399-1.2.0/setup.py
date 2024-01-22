import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis_Rijul_102103399", 
    version="1.2.0",
    author="Rijul",
    author_email="rjain_be21@thapar.edu",
    description="Automatic topsis for decision making",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    py_modules=["Topsis_Rijul_102103399","run"],
    packages=setuptools.find_packages(),
    
    keywords = ['command-line', 'topsis-python', 'TOPSIS'],  
    install_requires=[            
          'numpy',
          'pandas',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/topsis-101703382_cli"],
    python_requires='>=3.6',
)
