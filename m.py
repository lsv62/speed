import math
k=1.4
R=287.05287
ph=101325
pht=152258.6
print("Число M=", math.sqrt(2/(k-1)*((pht/ph)**((k-1)/k)-1)))
Th=288.15
print("Швидкість звуку a=", math.sqrt(k*R*Th))
rho=pht/R/Th
print("Густина повытря = ", rho)
print("Швидкість польоту", math.sqrt((104040.1-101325)/2/1.225))