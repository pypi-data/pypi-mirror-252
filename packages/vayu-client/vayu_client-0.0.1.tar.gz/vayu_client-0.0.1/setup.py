from setuptools import find_packages, setup

VERSION = "0.0.1"

setup(
    name="vayu_client",
    version=VERSION,
    description="Simple and easy to use python package for utilizing vayu billing system",
    python_requires='==3.7.*',
    author="Vayu, Inc.",
    author_email="team@withvayu.com",
    url="https://withvayu.com",
    keywords=["vayu", "billing", "events", "python", "sdk"],
    packages=find_packages(exclude=['*test']),
    # long_description="""\
    # The Vayu Event Ingestion client is a client that allows you to submit events for processing and storage. The client is designed to be effortlessly used by Vayu customers and partners to submit events from their own applications and systems. The client is secured using the Bearer Authentication scheme with JWT tokens. To obtain an access key token, please contact Vayu at team@withvayu.com
    # """,
    py_modules=['vayu', 'vayu_consts'],
)
