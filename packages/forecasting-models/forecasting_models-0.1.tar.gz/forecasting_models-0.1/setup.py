from setuptools import setup, find_packages

setup(
    name='forecasting_models',
    version='0.1',
    packages=find_packages(),
    description='Advanced Time Series Forecasting Suite: Leveraging Diverse Models for Predictive Analytics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kwadwo Daddy Nyame Owusu - Boakye',
    author_email='kwadwo.owusuboakye@outlook.com',
    url='https://github.com/knowusuboaky/forecasting_models',
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'statsmodels',
        'prophet',
        'xgboost'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords='forecasting time-series prophet xgboost random-forest mlp gradient-boosting',
)
