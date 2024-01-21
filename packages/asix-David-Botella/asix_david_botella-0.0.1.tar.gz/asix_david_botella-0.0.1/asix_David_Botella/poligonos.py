#David Botella Nicolás 2ºX ASIR
import math

class Circulo:
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return math.pi * self.radio ** 2

    def perimetro(self):
        return 2 * math.pi * self.radio

    def propiedades(self):
        return f"Círculo de radio {self.radio}: área = {self.area()}, perímetro = {self.perimetro()}"

class Cuadrado:
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2

    def perimetro(self):
        return 4 * self.lado

    def propiedades(self):
        return f"Cuadrado de lado {self.lado}: área = {self.area()}, perímetro = {self.perimetro()}"

class Triangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return 0.5 * self.base * self.altura

    def perimetro(self):
        return 2 * self.altura + self.base

    def propiedades(self):
        return f"Triángulo de base {self.base} y altura {self.altura}: área = {self.area()}, perímetro = {self.perimetro()}"

radio = float(input("Introduce el radio del círculo: "))
lado = float(input("Introduce el lado del cuadrado: "))
base = float(input("Introduce la base del triángulo: "))
altura = float(input("Introduce la altura del triángulo: "))

circulo = Circulo(radio)
cuadrado = Cuadrado(lado)
triangulo = Triangulo(base, altura)

print(circulo.propiedades())
print(cuadrado.propiedades())
print(triangulo.propiedades())