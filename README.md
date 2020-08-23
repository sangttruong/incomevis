<p align="center">
  <img width="100%" src="https://raw.githubusercontent.com/sangttruong/incomevis/master/logo.png" />
</p>

--------------------------------------------------------------------------------
[![License: MIT](https://img.shields.io/github/license/BayesWitnesses/m2cgen.svg)](https://github.com/sangttruong/IncomeVis/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/m2cgen.svg?logo=python&logoColor=white)](https://pypi.org/project/IncomeVis/)
[![PyPI Version](https://img.shields.io/pypi/v/m2cgen.svg?logo=pypi&logoColor=white)](https://pypi.org/project/IncomeVis/)
[![Downloads](https://pepy.tech/badge/incomevis)](https://pepy.tech/project/incomevis)

**[Documentation](https://pytorch-geometric.readthedocs.io)** | **[Paper](https://arxiv.org/abs/1903.02428)** | **[External Resources](https://cps.ipums.org/cps/)** | **[Use case examples](https://github.com/snap-stanford/ogb/tree/master/examples)**

Are you a _policy-maker_ who wants to see the dynamic of national income inequality? Are you a _researcher_ who want to visualize economic growth puzzles such as convergence? Or are you simply a _curious individual_ who want to figure out your position in the national income distribution? Wonder no more because we present `incomevis`, a library for income visualization (and more)!

Since income comparision is complicated, we offer _three default deflators_ (namely consumer price index, household size, and regional price parities) to bring the nominal income level to the real income level as much as we can. The income adjustment process is automatically handled for you. How convinient is that! If these deflators couldn't make you sastify, you can further adjust our deflated income if you have additional deflators. Also, if you like _interactive_ visualization, our graph can be display using JavaScript AmChart library. If you like _animated_ visualization, we offer a dynamically control animation of our graph based on Python Matplotlib library.

Happy visualizing economic complexity! 

## Installation
You can import this module with PIP:
```bash
$ python3 -m pip install incomevis
```

## Gallery

Interactive visualization in AmChart. More example of this type of graph is available at (https://research.depauw.edu/econ/incomevis)[https://research.depauw.edu/econ/IncIneq/index.html]
![logo](gallery/YEAR2018_HHINCOME.jpeg)

*   Dynamic animation
*   AmChart
*   Bootstrap


## Contact
Any question, feedback, or comment can be directed to [sangtruong_2021@depauw.edu](sangtruong_2021@depauw.edu) or [hbarreto@depauw.edu](hbarreto@depauw.edu). 

**TODO:**
- [ ] Get gif animation for readme
- [ ] change package name
- [ ] safe large file on git?
- [ ] update homepage
- [ ] comprehensively test for other functionality - percentile, bootstrap, etc
- [ ] marketing?
