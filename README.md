<p align="center">
  <img width="100%" src="https://raw.githubusercontent.com/sangttruong/incomevis/master/logo/logo.png" />
</p>

--------------------------------------------------------------------------------
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sangttruong/incomevis/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/incomevis?logo=python&logoColor=white)](https://pypi.org/project/incomevis/)
[![PyPI Version](https://img.shields.io/pypi/v/incomevis.svg?logo=pypi&logoColor=white)](https://pypi.org/project/incomevis/)
[![Downloads](https://pepy.tech/badge/incomevis)](https://pepy.tech/project/incomevis)

**[Paper V2](https://arxiv.org/abs/2108.03733)[, V1](https://ideas.repec.org/p/dew/wpaper/2020-03.html) | [Tutorial](https://colab.research.google.com/drive/1oebYZsoDHM8e0urOedVfjimrjvrxR-nY?usp=sharing) | [Documentation](https://incomevis.readthedocs.io/en/latest/) | [Website](https://research.depauw.edu/econ/incomevis/)** 

Are you a *policy-maker* who wants to see the dynamics of national income inequality? Are you a *researcher* who wants to visualize economic growth puzzles such as convergence? Or are you simply a *curious individual* who wants to see your position in the national income distribution? Wonder no more because we present *incomevis*, a library for income visualization (and more)!

Comparing incomes is complicated. We offer three default deflators (consumer price index, household size, and regional price parities) to adjust nominal household income. The income adjustment process is automatically handled for you. You can further adjust our deflated incomes if you have additional variables that you want to incorporate. Also, if you like *interactive* visualization, our graph can be displayed using JavaScript's amChart library. If you prefer an *animated* visualization, we offer a dynamically controlled animation of our graph based on Python Matplotlib library.

Happy visualizing economic complexity!

### News
* 01/2021: Our paper is presented at [National Collegiate Research Conference, Harvard University](https://www.hcura.org/about-ncrc).
* 03/2021: incomevis is presented at the Analytics Department at [Community Health Network](https://www.ecommunity.com/) for Black History Month.
* 08/2021: We use incomevis for a new course title [ECON390: Economics of Inequality](https://www.depauw.edu/academics/departments-programs/economics-management/courses/details/ECON/390/) at DePauw University.
* 08/2021: Help wanted! We are looking for maintainer for this project. Please contact [sttruong@cs.stanford.edu](sttruong@cs.stanford.edu) if you are interested.

## Installation

incomevis can be installed via pip:
```bash
$ pip install incomevis
```

## Authors and Acknowledgements
This project is co-authored by [Sang Truong](sangttruong.github.io, [sttruong@cs.stanford.edu](sttruong@cs.stanford.edu)) (Stanford University) and [Humberto Barreto](http://academic.depauw.edu/hbarreto_web/) (DePauw University, [hbarreto@depauw.edu](hbarreto@depauw.edu)). Please direct any question, feedback, or comment to either of the authors for support. This project was started in the summer 2019 under the support of Hewlett Mellon Presidential Fund for undergraduate research at DePauw University. We thank Frank Howland, Jonah Barreto, Jarod Hunt, and Bu Tran their support on preparing the manuscript.