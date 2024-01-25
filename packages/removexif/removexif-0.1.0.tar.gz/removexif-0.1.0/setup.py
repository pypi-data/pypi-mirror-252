from setuptools import setup, find_packages

setup(
    name='removexif',  # Replace with the actual name of your package
    version='0.1.0',  # Update with the version number
    description='Easily remove and add EXIF metadata to images',
    author='Tulio Bitencourt',
    author_email='tuliob.dev@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
)