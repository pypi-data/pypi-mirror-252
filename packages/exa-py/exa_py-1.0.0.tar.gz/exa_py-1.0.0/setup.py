from setuptools import setup, find_packages

setup(
    name='exa_py',
    version='1.0.0',
    description='Python SDK for Exa API.',
    author='Exa',
    author_email='hello@exa.ai',
    package_data={"exa_py": ["py.typed"]},
    url='https://github.com/exa-labs/exa-py',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Typing :: Typed",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
