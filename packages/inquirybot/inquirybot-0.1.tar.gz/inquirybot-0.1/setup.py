from setuptools import setup, find_packages

setup(
    name='inquirybot',
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
    package_data={
        'inquirybot': [
            'data/*.txt', 
            'data/*.csv',  # Include all .txt files inside the 'data' directory
            'models/*.pkl',  # Include all .pkl files inside the 'models' directory
        ]},
)
