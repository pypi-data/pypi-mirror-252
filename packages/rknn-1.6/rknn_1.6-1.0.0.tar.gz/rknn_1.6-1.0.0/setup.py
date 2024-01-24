from setuptools import setup, find_packages

setup(
    name='rknn_1.6',
    version='1.0.0',
    description='rknn_api',
    author='ErnisMeshi',
    author_email='ernis.meshi@student.uni-pr.edu',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    include_package_data=True,  # Include non-code files specified in MANIFEST.in
)

