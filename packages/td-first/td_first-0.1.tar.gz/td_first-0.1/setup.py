from setuptools import setup,find_packages 

setup(
    name='td_first',
      version='0.1',
      description='Gaussian distributions',
      packages = find_packages(),
      install_requires = [],
      author = "Tanya Dewland",
      author_email = "tanya.dewland@gmail.com",
      long_description = open("README.md").read(),
      long_description_content_type = "text/markdown",
      licence = "MIT",
      zip_safe=False)
