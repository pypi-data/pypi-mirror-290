# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybandits']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'numpy>=1.24.2,<2.0.0',
 'pydantic>=2.8.2,<3.0.0',
 'pymc>=5.3.0,<6.0.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'pybandits',
    'version': '0.4.0',
    'description': 'Python Multi-Armed Bandit Library',
    'long_description': "\nPyBandits\n=========\n\n![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/PlaytikaOSS/pybandits/continuous_integration.yml)\n![PyPI - Version](https://img.shields.io/pypi/v/pybandits)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybandits)\n![alt text](https://img.shields.io/badge/license-MIT-blue)\n\n**PyBandits**  is a ``Python`` library for Multi-Armed Bandit. It provides an implementation of stochastic Multi-Armed Bandit (sMAB) and contextual Multi-Armed Bandit (cMAB) based on Thompson Sampling.\n\nFor the sMAB, we implemented a Bernoulli multi-armed bandit based on Thompson Sampling algorithm [Agrawal and Goyal, 2012](http://proceedings.mlr.press/v23/agrawal12/agrawal12.pdf). If context information is available we provide a generalisation of Thompson Sampling for cMAB [Agrawal and Goyal, 2014](https://arxiv.org/pdf/1209.3352.pdf) implemented with [PyMC3](https://peerj.com/articles/cs-55/), an open source probabilistic programming framework  for automatic Bayesian inference on user-defined probabilistic models.\n\nInstallation\n------------\n\nThis library is distributed on [PyPI](https://pypi.org/project/pybandits/) and can be installed with ``pip``.\nThe latest release is version ``0.0.2``. ``pybandits`` requires a Python version ``>= 3.8``.\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash\npip install pybandits\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nThe command above will automatically install all the dependencies listed in ``requirements.txt``. Please visit the\n[installation](https://playtikaoss.github.io/pybandits/installation.html)\npage for more details.\n\nGetting started\n---------------\n\nA short example, illustrating it use. Use the sMAB model to predict actions and update the model based on rewards from the environment.\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~python\nimport numpy as np\nimport random\nfrom pybandits.core.smab import Smab\n\n# init stochastic Multi-Armed Bandit model\nsmab = Smab(action_ids=['Action A', 'Action B', 'Action C'])\n\n# predict actions\npred_actions, _ = smab.predict(n_samples=100)\n\nn_successes, n_failures = {}, {}\nfor a in set(pred_actions):\n\n    # simulate rewards from environment\n    n_successes[a] = random.randint(0, pred_actions.count(a))\n    n_failures[a] = pred_actions.count(a) - n_successes[a]\n\n    # update model\n    smab.update(action_id=a, n_successes=n_successes[a], n_failures=n_failures[a])\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nDocumentation\n-------------\n\nFor more information please read the full\n[documentation](https://playtikaoss.github.io/pybandits/pybandits.html)\nand\n[tutorials](https://playtikaoss.github.io/pybandits/tutorials.html).\n\nInfo for developers\n-------------------\n\nPyBandits is supported by the [AI for gaming and entertainment apps](https://www.meetup.com/ai-for-gaming-and-entertainment-apps/) community.\n\nThe source code of the project is available on [GitHub](https://github.com/playtikaoss/pybandits).\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash\ngit clone https://github.com/playtikaoss/pybandits.git\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nYou can install the library and the dependencies with one of the following commands:\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash\npip install .                        # install library + dependencies\npip install .[develop]               # install library + dependencies + developer-dependencies\npip install -r requirements.txt      # install dependencies\npip install -r requirements-dev.txt  # install developer-dependencies\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nAs suggested by the authors of ``pymc3`` and ``pandoc``, we highly recommend to install these dependencies with\n``conda``:\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash\nconda install -c conda-forge pandoc\nconda install -c conda-forge pymc3\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo create the file ``pybandits.whl`` for the installation with ``pip`` run the following command:\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash\npython setup.py sdist bdist_wheel\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo create the HTML documentation run the following commands:\n\n~~~~~~~~~~~bash\ncd docs\nmake html\n~~~~~~~~~~~\n\nRun tests\n---------\n\nTests can be executed with ``pytest`` running the following commands. Make sure to have the library installed before to\nrun any tests.\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash\ncd tests\npytest -vv                                      # run all tests\npytest -vv test_testmodule.py                   # run all tests within a module\npytest -vv test_testmodule.py -k test_testname  # run only 1 test\npytest -vv -k 'not time'                        # run all tests but not exec time\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nLicense\n-------\n\n[MIT License](LICENSE)\n",
    'author': "Dario d'Andrea",
    'author_email': 'dariod@playtika.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
