# python-nbody

### *N*-body simulator in Python

Simulates gravity between celestial bodies. Uses `pygame`.

---

### Command-line arguments
```
python3 python-nbody.py <WIDTH (optional)> <HEIGHT (optional)> <GRAVITATIONAL CONSTANT (optional)>
```
`WIDTH` - *optional (default: 1920)* - width of the simulator window

`HEIGHT` - *optional (default: 1080)* - height of the simulator window

`GRAVITATIONAL CONSTANT` - *optional (default: 1)* - sets the value of *G*; how strong the gravity is between objects

### The formulae
```python
for body in bodies:
    if body.index != self.index:
        dist_x = abs(body.x - self.x)
        dist_y = abs(body.y - self.y)
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

        force = G * (body.mass * self.mass / dist ** 2)

        if not self.stationary:
            self.xvel += (body.x - self.x) / dist * force
            self.yvel += (body.y - self.y) / dist * force

        if not body.stationary:
            body.xvel += (self.x - body.x) / dist * force
            body.yvel += (self.y - body.y) / dist * force
```
*(Lines 167-181)*
