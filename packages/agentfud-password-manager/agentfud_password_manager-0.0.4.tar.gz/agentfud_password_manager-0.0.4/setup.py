from setuptools import setup, find_packages
import os, pathlib
import pkg_resources

DESCRIPTION = 'AgentFUD Password Manager'

this_directory = pathlib.Path(__file__).parent.resolve()

with open(os.path.join(this_directory, 'README.md')) as readme:
    LONG_DESCRIPTION = readme.read()

with open(os.path.join(this_directory, 'requirements.txt')) as req:
    required = [
        str(rq) for rq in pkg_resources.parse_requirements(req)
    ]

setup(
    name="agentfud-password-manager",
    version="0.0.4",
    author='AgentFUD',
    author_email='agentfud@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    url='https://github.com/AgentFUD/agentfud-password-manager',
    keywords=['python', 'python3', 'Password manager', 'command line'],
    entry_points="""
        [console_scripts]
        af-password-manager=agentfud_password_manager.cli:cli
    """,
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   python_requires='>=3.1'
)
