from setuptools import setup, find_packages
setup(
    name="Pyvirertory",
    version="1.0.0",
    packages=find_packages(),
    description=("This third-party library makes it possible to quickly build simple virtual characters, have simple conversations "+
                 "with AI, and conduct personalized training. It's not particularly smart, but it's great for Python beginners."),
    package_data={
        "Pyvirertory": [r"Pyvirertory/Everykey.py", r"Pyvirertory/*"]
    },
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown"
)