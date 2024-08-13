from setuptools import setup, find_packages

__lib_name__ = "SpaGRA"
__lib_version__ = "1.0.0"
__description__ = "Relation-aware graph augmentation with geometric contrastive learning improves the domains identification from spatially resolved transcriptomics data"
__author__ = "Sun Xue"
__author_email__ = "sunxue_yy@mail.edu.sdu.cn"
__license__ = "MIT"
__keywords__ = ["Spatial transcriptomics", "Deep learning", "Domains identification"]
__requires__ = ["requests"]

setup(
    name=__lib_name__,
    version=__lib_version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    keywords=__keywords__,
    packages=find_packages(),
    install_requires=__requires__,
    zip_safe=False,
    include_package_data=True,
)
