from scipy.optimize import fsolve

import numpy.lib.scimath as math
def SyngasComposition_Calculations(T, Alfa, wC, wH, wO, wN, Beta, W):
    # Input Data
    # Temperature Reference (K)
    Tref = 298.15
    # Universal Constant (J/mol.K)
    R = 8.314
    # MolecularRelative
    mrC = 12
    mrH = 1
    mrO = 16
    mrN = 14
    # Komponen CH4
    ACH4 = 1.702
    BCH4 = 0.009081
    CCH4 = -0.000002164
    DCH4 = 0.0
    dH298CH4 = -74520
    dG298CH4 = -50460
    # Komponen CO
    ACO = 3.376
    BCO = 0.000557
    CCO = 0.0
    DCO = -3100
    dH298CO = -110525
    dG298CO = -137169
    # Komponen CO2
    ACO2 = 5.457
    BCO2 = 0.001045
    CCO2 = 0.0
    DCO2 = -115700
    dH298CO2 = -393509
    dG298CO2 = -394359
    # Komponen H2
    AH2 = 3.249
    BH2 = 0.000422
    CH2 = 0.0
    DH2 = 8300
    dH298H2 = 0.0
    dG298H2 = 0.0
    # Komponen N2
    AN2 = 3.28
    BN2 = 0.000593
    CN2 = 0.0
    DN2 = 4000
    dH298N2 = 0.0
    dG298N2 = 0.0
    # Komponen H2O
    AH2O = 3.47
    BH2O = 0.00145
    CH2O = 0.0
    DH2O = 12100
    dH298H2O = -241818
    dG298H2O = -228572

    def Mol_Unsur(w, W, mr):
        return w * W / mr

    FC = Mol_Unsur(wC, W, mrC) 
    FH = Mol_Unsur(wH, W, mrH)
    FO = Mol_Unsur(wO, W, mrO)
    FN = Mol_Unsur(wN, W, mrN)

    def Tta(F):
        F = Mol_Unsur(w, W, mr)
        return (2 * F) + (0.5 * F)

    Teta = (2 * FC) + (0.5 * FH)

    def Mol_O(F, Alfa, Teta):
        F = Mol_Unsur(w, W, mr)
        Teta = Tta(F)
        return F + (Alfa * Teta)

    BO = FO + (Alfa * Teta)

    def Mol_N(F, Alfa, Beta, Teta):
        F = Mol_Unsur(w, W, mr)
        Teta = Tta(F)
        return F + (Alfa * Beta * Teta)

    BN = FN + (Alfa * Beta * Teta)

    def Mol_CdanH(F):
        F = Mol_Unsur(w, W, mr)
        return F

    BC = FC
    BH = FH

    def idcph(A, B, C, D, T, Tref):
        Tau = T / Tref
        return (A + ((B / 2) * Tref * (Tau + 1)) + ((C / 3) * (Tref**2) * ((Tau**2) + Tau + 1)) + (D / (Tau * (Tref**2)))) * (T - Tref)

    ICPHCH4 = idcph(ACH4, BCH4, CCH4, DCH4, T, Tref)
    ICPHCO = idcph(ACO, BCO, CCO, DCO, T, Tref)
    ICPHCO2 = idcph(ACO2, BCO2, CCO2, DCO2, T, Tref)
    ICPHH2 = idcph(AH2, BH2, CH2, DH2, T, Tref)
    ICPHN2 = idcph(AN2, BN2, CN2, DN2, T, Tref)
    ICPHH2O = idcph (AH2O, BH2O, CH2O, DH2O, T, Tref)

    def idcps(A, B, C, D, T, Tref):
        Tau = T / Tref
        return (A + ((B * Tref) + ((C * Tref**2) + (D / (Tau**2 * Tref**2))) * ((Tau + 1) / 2)) * ((Tau - 1) / (math.log(Tau)))) * (math.log(Tau))

    ICPSCH4 = idcps(ACH4, BCH4, CCH4, DCH4, T, Tref)
    ICPSCO = idcps(ACO, BCO, CCO, DCO, T, Tref)
    ICPSCO2 = idcps(ACO2, BCO2, CCO2, DCO2, T, Tref)
    ICPSH2 = idcps(AH2, BH2, CH2, DH2, T, Tref)
    ICPSN2 = idcps(AN2, BN2, CN2, DN2, T, Tref)
    ICPSH2O = idcps(AH2O, BH2O, CH2O, DH2O, T, Tref)

    def dGf(dH298, dG298, T, Tref, R, ICPH, ICPS, A, B, C, D):
        ICPH = idcph(A, B, C, D, T, Tref)
        ICPS = idcps(A, B, C, D, T, Tref)
        return dH298 - (T / Tref) * (dH298 - dG298) + (R * ICPH) - (R * T * ICPS)

    dGfCH4 = dGf(dH298CH4, dG298CH4, T, Tref, R, ICPHCH4, ICPSCH4, ACH4, BCH4, CCH4, DCH4)
    dGfCO = dGf(dH298CO, dG298CO, T, Tref, R, ICPHCO, ICPSCO, ACO, BCO, CCO, DCO)
    dGfCO2 = dGf(dH298CO2, dG298CO2, T, Tref, R, ICPHCO2, ICPSCO2, ACO2, BCO2, CCO2, DCO2)
    dGfH2 = dGf(dH298H2, dG298H2, T, Tref, R, ICPHH2, ICPSH2, AH2, BH2, CH2, DH2)
    dGfN2 = dGf(dH298N2, dG298N2, T, Tref, R, ICPHN2, ICPSN2, AN2, BN2, CN2, DN2)
    dGfH2O = dGf(dH298H2O, dG298H2O, T, Tref, R, ICPHH2O, ICPSH2O, AH2O, BH2O, CH2O, DH2O)

    def Function_to_Solve(X):
        nCH4, nCO, nCO2, nH2, nN2, nH2O, lambdaC, lambdaH, lambdaO, lambdaN = X
        z1 = dGfCH4 + (R * T * (math.log(nCH4/(nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O)))) + lambdaC + (4 * lambdaH)
        z2 = dGfCO + (R * T * (math.log(nCO/(nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O)))) + lambdaC + lambdaO
        z3 = dGfCO2 + (R * T * (math.log(nCO2/(nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O)))) + lambdaC + (2 * lambdaO)
        z4 = (R * T * (math.log(nH2/(nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O)))) + (2 * lambdaH)
        z5 = (R * T * (math.log(nN2/(nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O)))) + (2 * lambdaN)
        z6 = dGfH2O + (R * T * (math.log(nH2O/(nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O)))) + (2 * lambdaH) + lambdaO
        z7 = nCH4 + nCO + nCO2 - BC
        z8 = (4 * nCH4) + (2 * nH2) + (2 * nH2O) - BH
        z9 = nCO + (2 * nCO2) + nH2O - BO
        z10 = nN2 - BN
        return (z1, z2, z3, z4, z5, z6, z7, z8, z9, z10)

    nCH40, nCO0, nCO20, nH20, nN20, nH2O0, lambdaC0, lambdaH0, lambdaO0, lambdaN0 = 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 1, 1, 1, 1
    guess = (nCH40, nCO0, nCO20, nH20, nN20, nH2O0, lambdaC0, lambdaH0, lambdaO0, lambdaN0)
    sol = fsolve(Function_to_Solve, guess)
    nCH4 = sol[0]
    nCO = sol[1]
    nCO2 = sol[2]
    nH2 = sol[3]
    nN2 = sol[4]
    nH2O = sol[5]

    def Mol_Total(n):
        return nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O

    ntotal = nCH4 + nCO + nCO2 + nH2 + nN2 + nH2O

    def Moles_Fraction(n, ntotal):
        ntotal = Mol_Total(n)
        return (n / ntotal) * 100

    yCH4 = Moles_Fraction(nCH4, ntotal)
    yCO = Moles_Fraction(nCO, ntotal)
    yCO2 = Moles_Fraction(nCO2, ntotal)
    yH2 = Moles_Fraction(nH2, ntotal)
    yN2 = Moles_Fraction(nN2, ntotal)
    yH2O = Moles_Fraction(nH2O, ntotal)

    return [yCH4, yCO, yCO2, yH2, yN2, yH2O]