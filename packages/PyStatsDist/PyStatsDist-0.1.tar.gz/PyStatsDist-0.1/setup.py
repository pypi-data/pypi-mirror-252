from setuptools import setup, find_packages

setup(name='PyStatsDist',
      version='0.1',
      description='Gaussian distributions',
      packages=find_packages(),
      install_requires=[
        'numpy',  # Add any dependencies your module requires
        'matplotlib',
      ],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      zip_safe=False)