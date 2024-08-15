from setuptools import setup, find_packages

setup(
    name='OfficelyTestTeam2',
    version='0.1.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically includes all packages
    include_package_data=True,  # Include additional files as specified in MANIFEST.in
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
