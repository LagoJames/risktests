## About credit-tests

**credit-tests** is a Python package that provides a set of statistical tests and tools to assess the performance of the credit risk models. The aim of the package is to provide all common tests used by today's modellers when developing, maintaining and validating their PD, LGD, EAD and prepayment models. All tests have been thoroughly tested and documented. Whenever possible, the definition of the test was retrieved from the authoritive source like EBA, ECB or Basel Committee.

The contributors started built their first statistical models in 2003. Over the years, the same tests have been implemented leading to inefficient usage of resources.

## Main Features
This is the list of main features:

  - tests cover both IFRS 9 and IRB models as well as non-regulatory models
  - the complete lists of tests is available here: [**all tests**][tests]
  - for the purpose of unit testing all tests have been implemented in [**Excel workbook**][tests]
  - the tests have been [**documented**][tests] in detail
  - [**commonly accepted tresholds**][tests] have been provided for convenience puproses
  
  
   [tests]:  https://aistat.com



## Where to get it
The source code is hosted on GitHub at:
https://github.com/aistat/credit-tests

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/credit-tests).

<code> pip install credit-tests </code>

## Documentation
The official documentation is hosted on pydocs.org: https://aistat.com

## Dependencies
- [NumPy - Adds support multi-dimensional arrays and high-level mathematical functions to operate on these arrays](https://www.numpy.org)
- [pandas - fundamental building block for doing practical, real world data analysis in Python](https://www.numpy.org)
- [statsmodels - provides functionality for the estimation of many different statistical models and tests](https://www.numpy.org)
- [Scikit-learn - provides various tools for model fitting, data preprocessing, model selection and model evaluation](https://www.numpy.org)



## Getting Help

For usage questions, the best thing is to send an email to anton.treialt@aistat.com

## Contributing to credit-tests
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

If you want to contribute to credit-tests, please review the
[contribution guidelines](CONTRIBUTING.md). This project adheres to this
[code of conduct](CODE_OF_CONDUCT.md). We use [GitHub issues](https://github.com/tensorflow/tensorflow/issues) for
tracking requests and bugs.



## License
[MIT](LICENSE)