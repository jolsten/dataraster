"""
This project's build structure
 - This project uses setuptools, so it is declared as the build system in the pyproject.toml file
 - We use as much as possible `setup.cfg` to store the information so that we can get some mandatory
   metadata in PKG-INFO that isn't possible with the pyproject.toml approach
See also:
  https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files
  https://stackoverflow.com/questions/73279327/how-to-indicate-use-scm-version-in-setup-cf
  https://github.com/smarie/python-genbadge
"""
from setuptools import setup
from setuptools.config import read_configuration

conf_dict = read_configuration("setup.cfg")
PKG_NAME = conf_dict['metadata']['name']

setup(
    # we can't put `use_scm_version` in setup.cfg yet unfortunately
    use_scm_version={
        "write_to": "src/%s/_version.py" % PKG_NAME,
    },  
)
