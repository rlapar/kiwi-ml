ML Weekend 
===================

Application iteratively request  data from server from interval [-n/2, n/2], with default distance 1 and default number of measurments of 5.

# Usage

```
python curveFitting.py [OPTION]
```

#### Options
**-i**: Path to json file to read the data from (instead of requesting the server interactively) - if specified, all other options are ignored

**-r**: Number of required measurments for one point - default 5

**-d**: Distance between the adjacent pair of points - default 1

**-n**: Number of points - default 500


Found function: 
![equation](https://latex.codecogs.com/gif.latex?f%28x%29%20%3D%20x%5E4%20-%205x%5E2%20&plus;%205x%20-%205)


**Author**: Radovan Lapár
