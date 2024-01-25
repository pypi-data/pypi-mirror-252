from setuptools import setup, find_packages

setup(
    name='chatbot_demo',
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
        'chatbot_demo': [
            'data/*.txt', 
            'data/*.csv',  # Include all .txt files inside the 'data' directory
            'models/*.pkl',  # Include all .pkl files inside the 'models' directory
        ]},
)
