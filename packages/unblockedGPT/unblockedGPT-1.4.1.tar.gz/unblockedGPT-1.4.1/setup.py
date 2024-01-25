from setuptools import setup, find_packages

setup(
    name='unblockedGPT',
    version='1.4.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'requests',
        'openai',
        'pycryptodome',  # This provides the Crypto module
    ],
    entry_points={
        'console_scripts': [
            'chatt = unblockedGPT.run_app:run',
        ],
    },
)
