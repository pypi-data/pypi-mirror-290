import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name         = "muti.basic",
  version      = "0.14.69",
  author       = "E.C.Ares",
  author_email = "E.C.Ares@outlook.com",
  url          = "https://github.com/E-C-Ares/muti.basic",
  description  = "muti for python",
  packages     = setuptools.find_packages(),
  classifiers  = [
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  long_description=long_description,
  long_description_content_type="text/markdown")