import setuptools
with open("README.md","r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="metacom-pkg-jobdiogenes",
    version="0.0.1",
    author="Job Diogenes Ribeiro Borges",
    author_email="jobdiogenes@gmail.com",
    description="Metacommunity Analysis",
    long_description=long_description,
    long_description_content_type="text/makdown",
    url="https://github.com/pypa/samplesproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)