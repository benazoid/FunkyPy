#FunkyPy

Welcome to the Funky Calculator! Made by Ben Richards - 10/9/23

This calculator takes in basically any function (see below), then parses and evaluates the given function. 
Simply run the main program and type your function into the console and have it compute. Don't use spaces,
that could mess it up. Funky uses no external computing resources besides the built in Python +, -, *, /, and %
operators. As well as many common algebraic functions, Funky also implements multiple tools for calculus, that can
compute integrals and approximate inverse functions using Newton's method. If you go into the main file, you can
even define variables and functions of your own.


List of functions/operators:


Operators (can use typical characters +-*/%)

add(a, b) - returns the sum a + b

sub(a, b) - returns the difference a - b

mult(a, b) - return the product a * b

div(a, b) - returns the quotient a / b

mod(a, b) - returns the modulus a % b


Basic Algebraic Functions

inv(x) - returns 1/x

sqrt(x) - returns the square root of x, the inverse of x^2

root(x, r) - returns rth root of x

intPow(x) - returns x^n, where n is an integer (is fast)

pow(x, p) - returns x^p, were p can be a float (is slow)

exp(x) - returns e^x, the exponential function, where e is euler's number (~2.716)

ln(x) - returns the natural logarithm of x, where the logarithm has a base of e (see exp(x))

log(x, b) - returns the log base b of x

abs(x) - returns the absolute value of x


Triginometric Functions

sin(x) - returns the sine of x

cos(x) - returns the cosine of x

tan(x) - returns the tangent of x


Calculus Stuff

riemannSum(funct, a, b, s) - retuns the riemann sum, an approximation of the integral, 
of the function funct from a to b, s being the amount of sections the sum is split into

inverseFunct(funct, deriv, x) - approximates the inverse of function funct, at x, using the derivative of funct (to 0.001%)
