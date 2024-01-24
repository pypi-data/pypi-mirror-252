from setuptools import setup, find_packages

setup(
    name='education_inquiry_package',
    version='0.3',
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
    package_data={'education-inquiry-package': ['data/*.txt']},
)
