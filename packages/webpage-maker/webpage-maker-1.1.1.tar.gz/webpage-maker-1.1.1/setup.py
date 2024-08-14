import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="webpage-maker",
  version="1.1.1",
  author="Chenfan Wang",
  author_email="admin@wcfstudio.cn",
  description="A Python library for generating (rendering) static HTML web pages",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/wang-chenfan/webpage-maker",
  packages=setuptools.find_packages(),
  classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
  ],
)