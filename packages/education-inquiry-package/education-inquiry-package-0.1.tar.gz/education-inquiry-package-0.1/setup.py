from setuptools import setup, find_packages

setup(
    name='education-inquiry-package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'joblib',
        'pandas',
        'numpy',
        'nltk',
        'torch',
        'transformers',
        'spellchecker',
        'gensim',
        'scikit-learn',
    ],
    package_data={'education-inquiry-package': ['data/*.bin', 'data/*.txt']},
)
