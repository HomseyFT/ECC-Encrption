#Finite field arithmetic over GF(p)
#All ECC operations happen modulo a prime p. This module provides
#the foundational modular arithmetic primitives.

def legendre_symbol(a: int, p: int) -> int:
    if p < 2 or not isinstance(p, int) or p % 2 == 0:
        raise ValueError("p is not an odd prime")

    a = a % p
    if a == 0:
        return 0

    result = pow(a, (p - 1) // 2, p)
    if result == p - 1:
        return -1
    else:
        return result

def calc_b(p: int) -> int:
    b = 2 
    attempts = 1 
    while legendre_symbol(b, p) == 1:
        b += 1
        attempts += 1 
    return b

def mod_inverse(a: int, p: int) -> int:    
    old_r,r = a % p, p
    old_s,s = 1,0 
    while r != 0:
        qotient = old_r // r
        old_r, r = r, old_r - qotient * r
        old_s, s = s, old_s - qotient * s
    if old_r != 1:
            raise ValueError(f"{a} has no inverse mod {p}")
    return old_s % p

def t_s_recursive(a: int, p: int, k: int, b: int, b_inverse: int) -> int:    
    m = (p - 1) >> k
    a_m = 1 
    while m % 2 == 0 and a_m == 1:
        m >>= 1 
        k += 1 
        a_m = pow(a, m, p)

    if a_m == p - 1:
        b_power = 1 << (k - 1)
        b_power_half = 1 << (k - 2)
        a_next = (a * pow(b, b_power, p)) % p
        a_next_root = t_s_recursive(a_next, p, k, b, b_inverse)
        a_root = a_next_root * pow(b_inverse, b_power_half, p)
        return a_root % p
    return pow(a, (m + 1) >> 1, p)

def t_s(a: int, p: int) -> int:
    if legendre_symbol(a, p) != 1:
        raise ValueError(f"{a} is not a square mod {p}")
    b = calc_b(p)
    b_inverse = mod_inverse(b, p)
    return t_s_recursive(a, p, 1, b, b_inverse)

    

print(mod_inverse(3,7)) # should be 5
print(t_s(
123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456790123456787654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654320987654321,16158503035655503650357438344334975980222051334857742016065172713762327569433945446598600705761456731844358980460949009747059779575245460547544076193224141560315438683650498045875098875194826053398028819192033784138396109321309878080919047169238085235290822926018152521443787945770532904303776199561965192760957166694834171210342487393282284747428088017663161029038902829665513096354230157075129296432088558362971801859230928678799175576150822952201848806616643615613562842355410104862578550863465661734839271290328348967522998634176499319107762583194718667771801067716614802322659239302476074096777926805531667726337)) # should be 62
print(legendre_symbol(2, 113)) # should be 1
print(calc_b(7))
