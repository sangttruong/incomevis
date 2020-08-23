# incomevis
[![GitHub Actions Status](https://github.com/BayesWitnesses/m2cgen/workflows/GitHub%20Actions/badge.svg?branch=master)](https://github.com/BayesWitnesses/m2cgen/actions)
[![Coverage Status](https://coveralls.io/repos/github/BayesWitnesses/m2cgen/badge.svg?branch=master)](https://coveralls.io/github/BayesWitnesses/m2cgen?branch=master)
[![License: MIT](https://img.shields.io/github/license/BayesWitnesses/m2cgen.svg)](https://github.com/BayesWitnesses/m2cgen/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/m2cgen.svg?logo=python&logoColor=white)](https://pypi.org/project/m2cgen)
[![PyPI Version](https://img.shields.io/pypi/v/m2cgen.svg?logo=pypi&logoColor=white)](https://pypi.org/project/m2cgen)
[![Downloads](https://pepy.tech/badge/m2cgen)](https://pepy.tech/project/m2cgen)

Are you a _policy-maker_ who wants to see the dynamic of national income inequality? Are you a _researcher_ who want to visualize economic growth puzzles such as convergence? Or are you simply a _curious individual_ who want to figure out your position in the national income distribution? Wonder no more because we present `incomevis`, a library for income visualization (and more)!

Since income comparision is complicated, we offer _three default deflators_ (namely consumer price index, household size, and regional price parities) to bring the nominal income level to the real income level as much as we can. The income adjustment process is automatically handled for you. How convinient is that! If these deflators couldn't make you sastify, you can further adjust our deflated income if you have additional deflators.

If you like _interactive_ visualization, our graph can be display using JavaScript AmChart library. If you like _animated_ visualization, we offer a dynamically control animation of our graph based on Python Matplotlib library.

Happy exploring the complexity of national income distribution via visualization!
