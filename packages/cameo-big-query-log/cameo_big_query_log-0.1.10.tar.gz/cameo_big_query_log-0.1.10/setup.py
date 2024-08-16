from setuptools import setup, find_packages

setup(
    name='cameo_big_query_log',
    version='0.1.10',
    packages=find_packages(),
    install_requires=[
        'google-cloud-bigquery',
        'cryptography',
        'pydantic'
    ],
    entry_points={
        'console_scripts': [
            'cameo_big_query_log=cameo_big_query_log.cameo_big_query_log:main',
        ],
    },
    author='bear',
    author_email='panda1993127@gmail.com',
    description='A package for logging data to Google BigQuery',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
