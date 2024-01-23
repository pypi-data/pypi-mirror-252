from setuptools import setup, find_packages

setup(
    name='psmoe',
    version='0.1.4.3',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.5',
        'matplotlib>=3.6.2',
        'opencv-python>=4.6.0.66',
        'nibabel>=5.2.0',
        'scipy>=1.9.3',
        'gdown>=4.7.3',
        'keras>=2.15.0',
        'tensorflow>=2.15.0'
    ],
    author='Martin Pierangeli',
    author_email='marespierangeli@gmail.com',
    description='A simple module for prostate segmentation of T2-W MRI sequences in Nifti format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mpierangeli/prostate_segmentation_moe', 
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='UNet, ML, Prostate, Segmentations',
    project_urls={
        'Source': 'https://github.com/mpierangeli/prostate_segmentation_moe',
    },
)
