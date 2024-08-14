from setuptools import setup

setup(
    name='leakyblobs',
    version='0.2.2',    
    description='Clustering leakage analysis library.',
    long_description=open("docs/README_PyPI.md").read(),
    long_description_content_type='text/markdown',
    url='https://git.equancy.cloud/equancy/data-intelligence/clustering_leakage_analysis/-/tree/1_initial_dev_HF',
    author='Hady Fawal',
    author_email='hfawal@equancy.com',
    license='Equancy All Rights Reserved',
    packages=['leakyblobs'],
    install_requires=['numpy>=1.26.1', 
                      'pandas>=2.0.0',
                      'openpyxl>=3.1.5',
                      'pyvis>=0.3.2',
                      'plotly>=5.20.0',
                      'scipy>=1.14.0',
                      'openpyxl>=3.1.5',
                      'setuptools>=72.1.0',
                      'scikit-learn>=1.5.1'              
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',     
        'Programming Language :: Python :: 3.11',
    ],
)
