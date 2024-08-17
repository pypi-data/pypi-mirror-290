from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xbern_confidence_intervals',
    version='1.0.0',
    author='Krishna Pillutla',
    author_email='krishnap@dsai.iitm.ac.in',
    description='Compute adaptive confidence intervals for XBern distributions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    url="https://github.com/krishnap25/xbern_confidence_intervals",
    project_urls={
        "Bug Tracker": "https://github.com/krishnap25/xbern_confidence_intervals/issues",
    },
    install_requires=[
        'numpy>=1.22.4',
        'pandas>=1.4.4',
        'scipy>=1.7.3'
    ],
)
