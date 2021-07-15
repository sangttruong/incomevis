<p align="center">
  <img width="100%" src="https://raw.githubusercontent.com/sangttruong/incomevis/master/logo/logo.png" />
</p>

--------------------------------------------------------------------------------
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sangttruong/incomevis/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/incomevis?logo=python&logoColor=white)](https://pypi.org/project/incomevis/)
[![PyPI Version](https://img.shields.io/pypi/v/incomevis.svg?logo=pypi&logoColor=white)](https://pypi.org/project/incomevis/)
[![Downloads](https://pepy.tech/badge/incomevis)](https://pepy.tech/project/incomevis)

**[Paper](https://github.com/sangttruong/incomevis/blob/gh-pages/incomevis.pdf)** | **[Colab Tutorial](https://colab.research.google.com/drive/1oebYZsoDHM8e0urOedVfjimrjvrxR-nY?usp=sharing)** | **[Documentation](https://incomevis.readthedocs.io/en/latest/)** | **[PyPI package](https://pypi.org/project/incomevis/)** |**[External Resources](https://cps.ipums.org/cps/)**

Are you a *policy-maker* who wants to see the dynamics of national income inequality? Are you a *researcher* who wants to visualize economic growth puzzles such as convergence? Or are you simply a *curious individual* who wants to see your position in the national income distribution? Wonder no more because we present *incomevis*, a library for income visualization (and more)!

Comparing incomes is complicated. We offer three default deflators (consumer price index, household size, and regional price parities) to adjust nominal household income. The income adjustment process is automatically handled for you. You can further adjust our deflated incomes if you have additional variables that you want to incorporate. Also, if you like *interactive* visualization, our graph can be displayed using JavaScript's amChart library. If you prefer an *animated* visualization, we offer a dynamically controlled animation of our graph based on Python Matplotlib library.

Happy visualizing economic complexity!

## Installation

incomevis can be installed via pip:
```bash
$ pip install incomevis
```

## Gallery

<div class="row">

<a href=https://research.depauw.edu/econ/incomevis/>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/interactive.png" height="135" width="405">
</a>

<a href=https://rb.gy/yiaexf>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/RHHINCOME.gif" height="135" width="405">
</a>

<a href=https://rb.gy/yiaexf>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/RHHINCOMEsorted.gif" height="135" width="405">
</a>

<a href=https://github.com/sangttruong/incomevis/blob/master/galery/DCrank.xlsx>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/RHHINCOMEsorted_DC.gif" height="135" width="405">
</a>
</div>

Interactive graph (top) and dynamic graph (bottom) is implement in JavaScript AmChart and Python Matplotlib, respectively. More instant examples of interactive graphs can be found at [research.depauw.edu/econ/incomevis](research.depauw.edu/econ/incomevis). Animated graphs with better control can be generated in a (preferably local) Python environment (for example, see [this notebook](https://colab.research.google.com/drive/1JtPi9w6ecJ-u8gdIiQlgcvgjWjb6XrpI?usp=sharing)).

4 levels of deflating income. 

<div class="row">

<a href=https://research.depauw.edu/econ/incomevis/>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/CA.png" height="135" width="405">
</a>

<a href=https://github.com/sangttruong/incomevis/blob/master/gallery/ranking.xlsx>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/DC.png" height="135" width="405">
</a>
</div>

Bellow are bootstrap resampling of 50p of DC in 1977 10000 times (bottom right) and 1 million times (bottom left). We also show the relative growth of CA and DC overtime. 
<div class="row">
<a href=https://github.com/sangttruong/incomevis/blob/master/gallery/ranking.xlsx>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/CArank.png" height="135" width="405">
</a>

<a href=https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/DCrank.png>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/DCrank.png" height="135" width="405">
</a>

<a href=https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/50p1977_11_1M.png>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/50p1977_11_1M.png" height="135" width="405">
</a>

<a href=https://rb.gy/yiaexf>
<img src="https://raw.githubusercontent.com/sangttruong/incomevis/master/gallery/50p1977_11_10K.png" height="135" width="405">
</a>

</div>

 A completed and separated page for gallery will be available soon! 

## Authors
* [Sang Truong](sangttruong.github.io) (Stanford University)
* [Humberto Barreto](http://academic.depauw.edu/hbarreto_web/) (DePauw University)

As this research is continue to evolve, please direct any question, feedback, or comment to [sttruong@stanford.edu](sttruong@stanford.edu) or [hbarreto@depauw.edu](hbarreto@depauw.edu).

## Acknowledgements
This project was started by Sang Truong and Humberto Barreto during summer 2019 under the support of Hewlett Mellon Presidential Fund for undergraduate research at DePauw University. We thank [Frank Howland](http://persweb.wabash.edu/facstaff/howlandf/) for his help in revising an early version of this paper. We thanks Jonah Barreto for writing the JavaScript code for this website. We thank [Bu Tran](https://github.com/hieumtran) for his help in displaying the 3D graph in python.
