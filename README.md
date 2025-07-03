# The integrality gap of the Traveling Salesman Problem is 4/3 if the LP solution has at most n+6 non-zero components

---

### **Tullio Villa,  Eleonora Vercesi, Janos Barta, Monaldo Mastrolilli**

This repository contains the code and data used in the paper:
_The integrality gap of the Traveling Salesman Problem is 4/3
if the LP solution has at most n+6 non-zero components_,
by Tullio Villa, Eleonora Vercesi, Janos Barta, Monaldo Mastrolilli.

The paper itself is included as ```paper.pdf```.


## Project Structure

The project is structures as follows.


- ```.```\
  The main directory stores modules with methods useful to reproduce the results of the paper:
  - ```stsp.py```
    implements the main methods for the symmetric traveling salesman problem;
  - ```ancestors.py```
    contains a simple method that checks whether a vertex is an ancestor;
  - ```optII.py```
    implements a procedure to solve OPTII;
  - ```bbmove.py```
    implements the BB-move and the associated construction of new walks;
  - ```GB_algorithm.py```
    implements the GB and GBe algorithms.

- ```vertices```\
  Contains ```txt``` files of the vertices: these are found on [Sylvia Boyd's website](https://www.site.uottawa.ca/~sylvia/subtourvertices/index.htm).

- ```ancestors```\
  Contains ```csv``` files of the ancestors.

- ```prod```\
  Contains modules for the production of the results presented in the paper.
  - ```retrieve_ancestors.py``` retrieves the ancestors from the vertices and stores them in the ```ancestors``` directory.
  - ```apply_GBe_algorithm.py``` applies the GBe algorithm to the ancestors and stores the results in the ```output``` directory.

```text 
.
│   ancestors.py
│   bbmove.py
│   GB_algorithm.py
│   optII.py
│   paper.pdf
│   README.md
│   stsp.py
├───ancestors
│       ancestors_3.csv
│       ancestors_4.csv
│       ancestors_5.csv
│       ancestors_6.csv
├───prod
│   │   apply_GBe_algorithm.py
│   │   retrieve_ancestors.py
│   └───output
│           GBe_on_ancestors_3.csv
│           GBe_on_ancestors_4.csv
│           GBe_on_ancestors_5.csv
│           GBe_on_ancestors_6.csv
└───vertices
        vertices_10.txt
        vertices_11.txt
        vertices_12.txt
        vertices_6.txt
        vertices_7.txt
        vertices_8.txt
        vertices_9.txt
```


## How to run the code

[//]: # (TODO)
TODO: add instructions on how to run the code: requirements, notebooks, ...
TODO: add the paper as well :)
