from setuptools import setup, find_packages

setup(
    name="avoDB",
    version="1.0.0",
    author="William Gaston",
    description="A CLI-based end-to-end encrypted database as a service with integrated messaging",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "argon2==0.1.10",
        "click==8.2.1",
        "keyring==23.5.0",
        "keyrings.alt==5.0.2",
        "psycopg2==2.9.10",
        "python-dotenv==1.1.1",
        "setuptools==59.6.0",
        "tabulate==0.9.0",
        "cryptography==3.4.8"
    ],
    entry_points={
        "console_scripts": [
            'avodb=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)