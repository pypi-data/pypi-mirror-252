name = "vads"

__version__ = "1.0.1.,21.01.2024"
__all__ = ["ARPES"]






from vads.base import *

print("-- vads {} --".format(__version__))
print("Visualization Arpes Data for Sirius")
#print("Taking A-branch analyzer workfunction = {}eV".format(ANALYZER_WORKFUNCTION))
print("By Rafael Reis Barreto. Email: rafinhareis17@gmail.com")
print("Sub-modules included:")
for name in __all__:
	print("\t",name)
