from setuptools import setup, find_packages

setup(
    name="verifyTelegram",
    version="0.1.0", 
    author="Mohammad Mohammadi Bijaneh", 
    author_email="hiostad6@gmail.com", 
    description="This Python module securely validates and extracts user data from a URL-encoded string, using HMAC and SHA-256 for data integrity. It features a User class to structure user information and a Data class for validation and data parsing. Ideal for web applications needing secure user authentication and data management, it's easy to integrate and use.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/D34DBOY/verifyTelegram.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.8',
    install_requires=[

    ],
)
