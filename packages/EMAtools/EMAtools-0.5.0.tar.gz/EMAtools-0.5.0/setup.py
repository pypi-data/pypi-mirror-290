from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
#long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="EMAtools",  # Required
    version="0.5.0",  # Required
    description="Python library for users of EMC Plus and Charge Plus.",  # Optional
    #long_description=long_description,  # Optional
    #long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/GriffinKowash/EMAtools",  # Optional
    author="Griffin Kowash",  # Optional
    author_email="griffin.kowash@ema3d.com",  # Optional
    package_dir={"": "src"},  # Optional
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7, <4",
    install_requires=["numpy", "scipy"],  # Optional
    project_urls={
        'Usage guide': 'https://github.com/GriffinKowash/EMAtools/blob/main/README.md',
        'GitHub': 'https://github.com/GriffinKowash/EMAtools',
        'Changelog': 'https://github.com/GriffinKowash/EMAtools/blob/main/CHANGELOG.md'
    }
)