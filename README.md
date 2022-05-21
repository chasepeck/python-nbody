# python-nbody

## *N*-body simulator in Python

Simulates gravity between celestial bodies.

---

### Command-line arguments
```
python3 python-nbody.py <WIDTH (optional)> <HEIGHT (optional)> <GRAVITATIONAL CONSTANT (optional)>
```
```WIDTH``` - *optional* - width of the simulator window

```HEIGHT``` - *optional* - height of the simulator window

```GRAVITATIONAL CONSTANT``` - *optional* - sets the value of *G*; how strong the gravity is between objects

### The math
<img src="https://latex.codecogs.com/png.image?\dpi{250}&space;\\d&space;=&space;\sqrt{|x_2&space;-&space;x_1|^2&space;&plus;&space;|y_2&space;-&space;y_1|^2}\\\\F&space;=&space;G\frac{m_1m_2}{d^2}\\\\v_1&space;=&space;\mathrm{Previous}&space;&plus;&space;F\frac{x_2&space;-&space;x_1}{d}\\\\v_2&space;=&space;\mathrm{Previous}&space;&plus;&space;F\frac{x_1&space;-&space;x_2}{d}&space;" title="N-body simulation formulae" />
