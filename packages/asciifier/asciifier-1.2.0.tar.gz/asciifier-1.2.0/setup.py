from setuptools import find_packages, setup

setup(
    name="asciifier",
    packages=find_packages(include=["asciifier"]),
    version="1.2.0",
    description="Converts an Image file into ASCII Art",
    author="jaiveer chadda",
    author_email='jaiveer.chadda@gmail.com',
    install_requires=["Pillow==10.1.0", "numpy==1.26.2", "requests==2.31.0"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
