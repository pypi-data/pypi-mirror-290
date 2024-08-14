from setuptools import setup, find_packages

setup(
    name='oct_tissuemasking',
    version='0.0.1',
    description='A PyTorch based package for automated OCT tissue masking.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Etienne Chollet',
    author_email='etiennepchollet@gmail.com',
    url='https://github.com/EtienneChollet/oct_tissuemasking',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'oct_tissuemasking=oct_tissuemasking:app'
            ]
        },
    install_requires=[
        'torch',
        'torchvision',
        'torchaudio',
        'torchmetrics',
        'cupy',
        'cupy-cuda116',
        'cyclopts',
        'jitfields',
        # 'synthspline @ git+https://github.com/balbasty/synthspline',
        'torch-interpol',
        'torch-distmap',
        'nibabel'
        # 'torch-interpol @ git+https://github.com/balbasty/torch-interpol',
        # 'torch-distmap @ git+https://github.com/balbasty/torch-distmap',
        # 'nibabel @ git+https://github.com/nipy/nibabel',
        'pytorch-lightning'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='~=3.9',
)
