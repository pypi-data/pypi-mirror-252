#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), "r", encoding="utf-8") as f:
    README = f.read()

with open(os.path.join(here, "requirements.txt")) as f:
    install_reqs = f.read()

with open(os.path.join(here, "dev_requirements.txt")) as f:
    dev_requirements = [pkg.strip() for pkg in f.read().splitlines() if pkg.strip()]

with open(os.path.join(here, "CURRENT_VERSION")) as f:
    current_version = f.read().splitlines()[0].strip()

entry_points = {
    "paste.app_factory": [
        "main=endi:main",
    ],
    "console_scripts": [
        "endi-migrate = endi.scripts:migrate_entry_point",
        "endi-admin = endi.scripts:admin_entry_point",
        "endi-cache = endi.scripts:cache_entry_point",
        "endi-clean = endi.scripts:clean_entry_point",
        "endi-export = endi.scripts:export_entry_point",
        "endi-custom = endi.scripts.endi_custom:custom_entry_point",
        "endi-company-export = endi.scripts:company_export_entry_point",
        "endi-anonymize = endi.scripts:anonymize_entry_point",
        "endi-load-demo-data = endi.scripts:load_demo_data_entry_point",
    ],
    "fanstatic.libraries": ["endi = endi.resources:lib_endi"],
}

setup(
    name="moogli-erp",
    version=current_version,
    description="Progiciel de gestion pour CAE",
    long_description=README,
    long_description_content_type="text/x-rst",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Majerti",
    author_email="contact@majerti.fr",
    keywords="pyramid,business,web",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",  # keep in sync with pyproject.toml
    install_requires=install_reqs,
    tests_require=["pytest", "WebTest", "Mock"],
    extras_require={"dev": dev_requirements},
    setup_requires=[],
    test_suite="endi.tests",
    entry_points=entry_points,
)
