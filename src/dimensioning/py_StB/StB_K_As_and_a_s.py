###----DIMENSIONING OF CIRCULAR REINFORCEMNT-----###
'''
Date of Original Version -26th July, 2017 -
Date of Python version - 6th Feb, 2020 - ----
'''
###----Python Version created by RAGADEEP BOJJA (Translate of 0_stb created in VBA by Dr. Berthold Klobe)----###
#------------------------------------------------------------------------------------------------------#
#
#Required Modules
import math 
#import GlobalVar as Variable
from src.dimensioning.py_StB import GlobalVar as Variable
#Constants for Threshold stress limits for stboNorm = 0 (DIN 1045:1988)#
stbkitmax = 50
stbkepse3 = 0.0001
stbkepse5 =0.00001
stbkepse7 = 0.0000001
#stbofck (beta_WN) = 15
stbk15tau012 = 0.5
stbk15tau02 = 1.2
stbk15tau03 = 2
stbk15tau1 = 1.4           #Verbundbereich I
stbk15tau2 = 0.7           #Verbundbereich II
#stbofck (beta_WN) = 25
stbk25tau012 = 0.75
stbk25tau02 = 1.8
stbk25tau03 = 3
stbk25tau1 = 1.8           #Verbundbereich I
stbk25tau2 = 0.9           #Verbundbereich II
#stbofck (beta_WN) = 35
stbk35tau012 = 1
stbk35tau02 = 2.4
stbk35tau03 = 4
stbk35tau1 = 2.2           #Verbundbereich I 
stbk35tau2 = 1.1           #Verbundbereich II
#stbofck (beta_WN) = 45
stbk45tau012 = 1.1
stbk45tau02 = 2.7
stbk45tau03 = 4.5
stbk45tau1 = 2.6           #Verbundbereich I
stbk45tau2 = 1.3           #Verbundbereich II
#stbofck (beta_WN) = 55
stbk55tau012 = 1.25
stbk55tau02 = 3
stbk55tau03 = 5
stbk55tau1 = 3             #Verbundbereich I 
stbk55tau2 = 1.5           #Verbundbereich II

# Fixed Values #
# Gaping gap:
# Regardless of the selected standard, the regulation from DIN EN 1992-1-1: 2004 + AC: 2010 + NA: 2011 (stboNorm = 3) is applied uniformly.
# This regulation says that in the unreinforced rectangular cross-section, a center to the maximum e = 0.4 * stboD is permitted for the design internal forces.
# This corresponds to an elongation eps_c1 / eps_c2 = -0.35% / 1.105%. For circular cross sections, this elongation state is reached for e = 0.3803 * stboD.
stbkKemax = 0.3803
stbkRemax = 0.4
#------------------------------------------------------------------------------------------------------#
'''
# stboNorm:      0 = DIN 1045:1988
#                1 = DIN 1045:2008
#                2 = EN 1992-1-1:2004  (Eurocode 2)
#                3 = DIN EN 1992-1-1:2004 + AC:2010 + NA:2011
'''
#------------------------------------------------------------------------------------------------------#
##############################----Input and output values###############################################
#------------------------------------------------------------------------------------------------------#  
'''
# Input and output values
# Norm: 0 = DIN 1045: 1988
# 1 = DIN 1045: 2008
# 2 = EN 1992-1-1: 2004 (Eurocode 2)
# 3 = DIN EN 1992-1-1: 2004 + AC: 2010 + NA: 2011

# gam_c: safety factor / partial safety factor for concrete (depending on standards) [1]
# gam_s: partial safety factor for reinforcement (only for norm> 0) [1]

# Md: design value of the bending moment, negative values ​​result in tension for As2 [kNm]
# ND: design value of normal force, tension positive, pressure negative [kN]
# QD: design value of the shear force [kN]

# DD: circle diameter [mm]
# HH_: edge distance of the reinforcement [mm]
# vorAs0: existing reinforcement As [cm ^ 2]

# f_ck: Concrete compressive strength (cube strength for standard = 0, cylinder strength for standard> 0) [MN / m ^ 2]
# alpha: reduction factor for the concrete compressive strength [1]
# eps_cy: start of plastic concrete expansion (end of the parabola branch) [1]
# eps_cu: elongation at break of the concrete (end of plastic compression) [1]
# n2: parabola exponent of the concrete [1]
# delt_S: Increased safety for pressed concrete cross section / unreinforced concrete (depending on the standard) [1]
# delt_K: associated expansion range / proportion of the compressive force that must be covered by reinforcement (depending on the standard) [String]

# f_yk: yield strength of the reinforcement [MN / m ^ 2]
# f_tk: tensile strength of the reinforcement [MN / m ^ 2]
# Es: Young's modulus of reinforcement [MN / m ^ 2]
# eps_su: elongation at break of the reinforcement (end of plastic elongation) [1]

# TauP1: for norm = 0: specification of tau_012 [MN / m ^ 2]
# TauP2: for norm = 0: specification of tau_02 [MN / m ^ 2]
# TauP3: for norm = 0: specification of tau_03 [MN / m ^ 2]

# for norm> 0: specification of cot (theta), min. 1.00, max. 3.00 [1]

# ii: Switch for the return value
# 11 = concrete compressive force [kN]
# 12 = lever arm of the concrete pressure force [mm]
# 13 = steel tensile force [kN]
# 14 = lever arm of steel tensile force [mm]
# 15 = steel pressure force [kN]
# 16 = lever arm of the steel pressure force [mm]
# 17 = resulting pair of forces [kN]
# 18 = lever arm of the resulting pair of forces [mm]
# 19 = required shear reinforcement stbZerfas [cm ^ 2 / m]
# stbZerfas = -1 #: impermissibly high shear load
# for norm = 0
# 20 = tau_0 [MPa]
# 21 = tau_012 [MPa]
# 22 = tau_02 [MPa]
# 23 = tau_03 [MPa]
# for norm> 0
# 20 = stbZminas [cm ^ 2 / m]
# 21 = stbZVRdc [kN]
# reinforced cross section
# 22 = stbZVRdmax [kN]
# 23 = stbZcottheta [1]
# unreinforced cross section
# 22 = stbZtaucp [MPa]
# 23 = stbZfcvd [MPa]
'''
#------------------------------------------------------------------------------------------------------#
#################################----Input Functions----################################################
#------------------------------------------------------------------------------------------------------# 

def StB_K_MN(Norm, gam_c, gam_s, Md, Nd, Mk,Nk ,DD, HH_, vorAs0 ,f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K,f_yk, f_tk, Es, eps_su, RissP1, minBew,ii):
    # Function that calculates the Longitudinal reinforcement Dimensions of the Desired Circular cross- section
    mue0 = [0,0,0]

    # Evidence and cross section
    Variable.stboNachweis = 1
    Variable.stboQuer = 1

    RechenWerte(Norm, gam_c, gam_s, Md, Nd, 0, Mk, Nk, DD, 0, HH_, HH_, True, vorAs0, 0, 0, 0,f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, RissP1, minBew, 0, 0, 0, ii)

    if Variable.stbZbFehler ==  True : 
        print('error = ',Variable.stbZbFehler)
    
    # Determination of the fracture condition: safety factors, strains, internal forces, associated lever arms
    if Variable.stboNullSd ==  True :
        Variable.stbZerfmue0[0] = 0
        Variable.stbZmue0[0] = Variable.stbovormue0[0]
        if Variable.stbobminBew ==  True :
            Variable.stbZmue0[0] = max(Variable.stbZmue0[0], Variable.stbomue0Riss[0])

    else:
        if Variable.stbobDruc[2] == True and Variable.stbovormue0[0] <= stbkepse7 and Variable.stbobminBew == False :
            Snue0_K()
            if Variable.stbZnue0 > 0 :
                Variable.stbZerfmue0[0] = 0
                Variable.stbZmue0[0] = 0
                
        else:
            Variable.stbZnue0 = -1

        if Variable.stbZnue0 < 0 :
            SRissB()

    # Conditions to give the output
    # Inputs must be specified properly to get correct outputs
    if Variable.stbZbFehler :
        StB_K_Mn = "Error[0]"

    elif Variable.stboii == 11 :
        # ultimate strain of concrete    ε_c		
        StB_K_Mn = Variable.stbZepscd[1 + Variable.stboVMd]

    elif Variable.stboii == 12 :
        # ultimate strain of concrete    ε_c
        StB_K_Mn = Variable.stbZepscd[2 - Variable.stboVMd]

    elif Variable.stboii == 13 :
        # ultimate strain of steel         ε_s		
        if Variable.stbZmue0[0] < stbkepse7 :
            StB_K_Mn = ""
        else:
            StB_K_Mn = Variable.stbZepssd[1 + Variable.stboVMd]

    elif Variable.stboii == 14 :
        # ultimate strain of steel         ε_s
        if Variable.stbZmue0[0] < stbkepse7 :
            StB_K_Mn = ""
        else:
            StB_K_Mn = Variable.stbZepssd[2 - Variable.stboVMd]

    elif Variable.stboii == 15 :
        #internal forces R_Md [KNm]	
        StB_K_Mn = math.copysign(1,Md) * Variable.stbZRMd * 1000 * Variable.stboKR ** 3 * Variable.stbofck

    elif Variable.stboii == 16 :
        #internal forces R_Nd [KN]	
        StB_K_Mn = Variable.stbZRNd * 1000 * Variable.stboKR ** 2 * Variable.stbofck

    elif Variable.stboii == 17 :
        #Reinforcement Area A_s [cm2]
        StB_K_Mn = 10000 * Variable.stbZmue0[0] * math.pi * Variable.stboKR ** 2 * Variable.stbofck / Variable.stboftk

    elif Variable.stboii == 19 :
        # utilization   =   req. A_s / A_s		
        if Variable.stboNullSd :
            StB_K_Mn = 0
        else:
            if Variable.stbZmue0[0] < stbkepse7 :
                StB_K_Mn = Variable.stboNd / Variable.stbZRNd
            else:
                if vorAs0 < stbkepse7 :
                    StB_K_Mn = max(Variable.stbZerfmue0[0], 0) / Variable.stbZmue0[0]
                else:
                    mue0[0] = Variable.stbZmue0[0]
                    StB_K_Mn = StB_K_MN(Norm, gam_c, gam_s, Md, Nd, Mk, Nk,DD, HH_, 0,f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, 0, minBew, 17)/ 10000 / math.pi / Variable.stboKR ** 2 / Variable.stbofck * Variable.stboftk / mue0[0]
    
    # Stbziz = 2 from here (Cracked Concrete)
    elif Variable.stboii == 21 :
        # strain of concrete   ε_c
        StB_K_Mn = Variable.stbZepsck[1 + Variable.stboVMk]

    elif Variable.stboii == 22 :
        # strain of concrete   ε_c
        StB_K_Mn = Variable.stbZepsck[2 - Variable.stboVMk]

    elif Variable.stboii == 23 :
        # strain of steel     ε_s	
        if Variable.stbZmue0[0] < stbkepse7 :
            StB_K_Mn = ""
        else:
            StB_K_Mn = Variable.stbZepssk[1 + Variable.stboVMk]

    elif Variable.stboii == 24 :
        # strain of steel     ε_s
        if Variable.stbZmue0[0] < stbkepse7 :
            StB_K_Mn = ""
        else:
            StB_K_Mn = Variable.stbZepssk[2 - Variable.stboVMk]

    elif Variable.stboii == 25 :
        #internal forces R_Mk [KNm]
        StB_K_Mn = math.copysign(1,Mk) * Variable.stbZRMk * 1000 * Variable.stboKR ** 3 * Variable.stbofck

    elif Variable.stboii == 26 :
        #internal forces R_Nk [KN]
        StB_K_Mn = Variable.stbZRNk * 1000 * Variable.stboKR ** 2 * Variable.stbofck

    elif Variable.stboii == 27 :
        #reinforce. stress σs [MPa]	
        if Variable.stbZmue0[0] < stbkepse7 :
            StB_K_Mn = ""
        else:
            StB_K_Mn = stbfsig_s(Variable.stbZepssk[1 + Variable.stboVMk])

    elif Variable.stboii == 28 :
        #reinforce. stress σs [MPa]	
        if Variable.stbZmue0[0] < stbkepse7 :
            StB_K_Mn = ""
        else:
            StB_K_Mn = stbfsig_s(Variable.stbZepssk[2 - Variable.stboVMk])

    else:
        StB_K_Mn = ""

    return StB_K_Mn
#------------------------------------------------------------------------------------------------------#  
    
def StB_K_Q(Norm, gam_c, gam_s, Md, Nd, Qd, DD, HH_, vorAs0, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, TauP1, TauP2, TauP3, ii):
    # Function that calculates the Shear reinforcement Dimensions of the Desired Circular cross- section

    RechenWerte(Norm, gam_c, gam_s, Md, Nd, Qd, 0, 0, DD, 0, HH_, HH_, False, vorAs0, 0, 0, 0, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, 0, 0, TauP1, TauP2, TauP3, ii)
    
    if Variable.stbZbFehler :
         print('error = ',Variable.stbZbFehler)

    # # Determination of the fracture condition: safety factors, strains, internal forces, associated lever arms
    if not Variable.stboNullSd :
        BruchC1S1()

    if Variable.stboNorm == 0 :
        QuerBemessN0()
    elif Variable.stboNorm > 0 :
        QuerBemessN123()

    # Conditions to give the output
    # Inputs must be specified properly to get correct outputs
    if Variable.stbZbFehler == True :
        StB_K_Q = "Error[0]"

    elif Variable.stboii == 11 :
        # Internal Force [kN] - C_Cu
        if Variable.stbZNucs[0] > -stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = Variable.stbZNucs[0] * 1000 * Variable.stboKR ** 2 * Variable.stbofck

    elif Variable.stboii == 12 :
        # Lever Arm [mm] - C_Cu
        if Variable.stbZNucs[0] > -stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = math.copysign(1,Md) * Variable.stbZzi[0] * 1000

    elif Variable.stboii == 13 :
        # Internal Force [kN] - T_Su
        if Variable.stbZNucs[1] < stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = Variable.stbZNucs[1] * 1000 * Variable.stboKR ** 2 * Variable.stbofck

    elif Variable.stboii == 14 :
        # Lever Arm [mm] - T_Su
        if Variable.stbZNucs[1] < stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = math.copysign(1,Md) * Variable.stbZzi[1] * 1000

    elif Variable.stboii == 15 :
        # Internal Force [kN] - C_Su
        if Variable.stbZNucs[2] > -stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = Variable.stbZNucs[2] * 1000 * Variable.stboKR ** 2 * Variable.stbofck

    elif Variable.stboii == 16 :
        # Lever Arm [mm] - C_Su
        if Variable.stbZNucs[2] > -stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = math.copysign(1,Md) * Variable.stbZzi[2] * 1000

    elif Variable.stboii == 17 :
        # Internal Force [kN] - Couple of Forces
        if Variable.stbZNucs[3] < stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = Variable.stbZNucs[3] * 1000 * Variable.stboKR ** 2 * Variable.stbofck

    elif Variable.stboii == 18 :
        # Lever Arm [mm] - Couple of Forces
        if Variable.stbZNucs[3] < stbkepse7 :
            StB_K_Q = ""
        else:
            StB_K_Q = Variable.stbZzi[3] * 1000

    elif Variable.stboii == 19 :
        # shear reinforce.   req. a_s [cm²/m]		
        StB_K_Q = Variable.stbZerfas
        
    elif Variable.stboii == 20 :
        # min. a_s    [cm²/m]	
        if Variable.stboNorm == 0 :
            StB_K_Q = Variable.stbZtau0
        else:
            StB_K_Q = Variable.stbZminas

    elif Variable.stboii == 21 :
        # V_Rdc [KN]
        if Variable.stboNorm == 0 :
            StB_K_Q = Variable.stbotau012
        else:
            StB_K_Q = Variable.stbZVRdc * 1000

    elif Variable.stboii == 22 :
        # V_Rdmax [KN]
        if Variable.stboNorm == 0 :
            StB_K_Q =Variable.stbotau02
        else:
            if Variable.stbZmue0[0] < stbkepse7 :
                StB_K_Q = Variable.stbZtaucp
            else:
                StB_K_Q = Variable.stbZVRdmax * 1000

    elif Variable.stboii == 23 :
        # cot(θ) [1]
        if Variable.stboNorm == 0 :
            StB_K_Q = Variable.stbotau03
        else:
            if Variable.stbZmue0[0] < stbkepse7 :
                StB_K_Q = Variable.stbZfcvd
            else:
                StB_K_Q = Variable.stbZcottheta

    else:
        StB_K_Q = ""
        
    return StB_K_Q

#------------------------------------------------------------------------------------------------------#  
#------------------------------------------------------------------------------------------------------#
#################################----Module Begins Here----#############################################
#------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------#
def RechenWerte(Norm, gam_c, gam_s, Md, Nd, Qd, Mk, Nk,DD, BB, HH_, H__, sym0 , vorAs0, delta, vorAs1, vorAs2, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K,f_yk, f_tk, Es, eps_su, RissP1, minBew, TauP1, TauP2, TauP3, ii):

    #Norm
    Variable.stboNorm = Norm
    Variable.stboQuer = 1

    #Geometry
    Variable.stboD = DD / 1000
    Variable.stboRB = BB / 1000
    Variable.stboKR = Variable.stboD / 2
    Variable.stboH[1] = HH_ / 1000
    Variable.stboH[2] = H__ / 1000
    Variable.stboRe = Variable.stboKR - Variable.stboH[1]
    Variable.stbodelt2 = delta / 2
    if abs(Variable.stboH[1] - Variable.stboH[2]) > stbkepse5:
        Variable.stbobHkrit = True
    else:
        Variable.stbobHkrit = False
    
    #Concrete
    Variable.stbofck = f_ck
    Variable.stboalpha = alpha
    Variable.stboepscy = eps_cy
    Variable.stboepscu = eps_cu
    Variable.stbon2 = n2

    #Reinforcement (Steel)
    Variable.stbofyk = f_yk
    Variable.stboftk = f_tk
    Variable.stboepssy = f_yk / Es
    Variable.stboepssu = eps_su
    Variable.Nd1 = Nd

    #Dimensionless Internal Forces
    Variable.stboNd = Variable.Nd1 / 1000 / Variable.stboKR ** 2 / Variable.stbofck
    Variable.stboMd = abs(Md) / 1000 / Variable.stboKR ** 3 / Variable.stbofck
    Variable.stboQd = abs(Qd) / 1000 / Variable.stboKR ** 2 / Variable.stbofck
    Variable.stboNk = Nk / 1000 / Variable.stboKR ** 2 / Variable.stbofck
    Variable.stboMk = abs(Mk) / 1000 / Variable.stboKR ** 3 / Variable.stbofck
    Variable.stboHQ = Variable.stboD * math.sqrt(math.pi / 4)
    Variable.stboBQ = Variable.stboD * math.sqrt(math.pi / 4)

    #LoadfromMiddle
    if abs(Variable.stboNd) < stbkepse7:
        Variable.stboeNd = Variable.stboMd / stbkepse7
    else:
        Variable.stboeNd = Variable.stboMd / Variable.stboNd
    
    if abs(Variable.stboNk) < stbkepse7:
        Variable.stboeNk = Variable.stboMk / stbkepse7
    else:
        Variable.stboeNk = Variable.stboMk / Variable.stboNk

    #Intiating Zero pressures
    if abs(Variable.stboNd) < stbkepse5 and Variable.stboMd < stbkepse5:
        #For DesignForces
        Variable.stboNullSd = True
        Variable.stboVMd = 0
        #For Characteristic Forces
        Variable.stboNullSk = True
        Variable.stboVMk = 0
    else:
        #For DesignForces
        Variable.stboNullSd = False
        if Md >= 0:
            Variable.stboVMd = 0
        else:
            Variable.stboVMd = 1
        
        #For DesignForces
        if abs(Variable.stboNk) < stbkepse5 and Variable.stboMk < stbkepse5:
            Variable.stboNullSk = True
        else:
            Variable.stboNullSk = False
            if Mk >= 0:
                Variable.stboVMk = 0
            else:
                Variable.stboVMk = 1

        #Pressure bar (stbobDruc) Boolean
        if Variable.stboNd < -stbkepse5:
            Variable.stbobDruc[1] = True
            if (((Variable.stboQuer == 1 or Variable.stboQuer == 2) and Variable.stboMd / abs(Variable.stboNd) < 1) or (Variable.stboQuer == 3 and Variable.stboMd/abs(Variable.stboNd) < 0.5)):
                Variable.stbobDruc[2] = True
                if ((Variable.stboQuer == 1 or Variable.stboQuer == 2) and Variable.stboMd / abs(Variable.stboNd) < 2 * stbkKemax)or(Variable.stboQuer == 3 and Variable.stboMd / abs(Variable.stboNd) < stbkRemax):
                    Variable.stbobDruc[3] = True
                else:
                    Variable.stbobDruc[3] = False
                
            else:
                Variable.stbobDruc[2] = False
                Variable.stbobDruc[3] = False
            
        else:
            Variable.stbobDruc[1] = False
            Variable.stbobDruc[2] = False
            Variable.stbobDruc[3] = False
        
    #Specified Reinforcement (Basic and Minimum)
    if Variable.stboNachweis == 1:
        vAs1 = max(vorAs1, vorAs2)
        vAs2 = min(vorAs1, vorAs2)
    elif Variable.stboNachweis == 2:
        vAs1 = vorAs1
        vAs2 = vorAs2

    if Variable.stboQuer == 1 or Variable.stboQuer == 2:
        Variable.stbovormue0[0] = max(vorAs0 / 10000 / math.pi / Variable.stboKR ** 2 * Variable.stboftk / Variable.stbofck, 0)
        Variable.stbovormue0[1] = max(vAs1 / 10000 / math.pi / Variable.stboKR ** 2 * Variable.stboftk / Variable.stbofck, 0)
        Variable.stbovormue0[2] = max(vAs2 / 10000 / math.pi / Variable.stboKR ** 2 * Variable.stboftk / Variable.stbofck, 0)
    elif Variable.stboQuer == 3:
        Variable.stbovormue0[0] = 0
        Variable.stbovormue0[1] = max(vAs1 / 10000 / Variable.stboD / Variable.stboRB * Variable.stboftk / Variable.stbofck, 0)
        Variable.stbovormue0[2] = max(vAs2 / 10000 / Variable.stboD / Variable.stboRB * Variable.stboftk / Variable.stbofck, 0)
    
    if sym0:
        Variable.stbovormue0[2] = Variable.stbovormue0[1]
    
    #Basic values ​​of the safety factors and auxiliary variables
    SgamCSini(gam_c, gam_s, delt_S, delt_K)

    # Without torque stress (or stboeNd = stbfeBew) or with an unequal sign of the moments for design and
    # Usage internal forces or by default, the statically required reinforcement is symmetrical.
    # For uneven edge distances of the reinforcement (stbobHkrit = True) and stbosymmue0 = True exists for (almost) centric
    # Tensile load is not a solution. Therefore this case is excluded.
    Variable.stbZiZ = 1                  
    # The function stbfeBew() is executed with fractional values from geometry
    if (abs(Variable.stboeNd - stbfeBew()) < stbkepse7 and Variable.stboNd > stbkepse5) or (abs(Variable.stboeNd) < stbkepse7 and Variable.stboNd < -stbkepse5) or((Variable.stboVMd != Variable.stboVMk or sym0 == True) and Variable.stbobHkrit == False):
        Variable.stbosymmue0 = True
    else:
        Variable.stbosymmue0 = False

    # Crack width limitation: maximum steel tension when in use, 
    # stboRissP1 <1 # -> no crack width limitation
    Variable.stboRissP1 = RissP1

    # '' Critical strain states are required for the iterative determination of the equilibrium states
    Variable.stbZiZ = 1   # The Sdehnkrit routine is carried out with fractional values         
    Sdehnkrit()

    # Minimum reinforcement (stbZmue0> = stbomue0Riss)
    if Variable.stboNachweis == 1:
        # Determination of the minimum reinforcement stbomue0Riss for the crack moment
        Smue0Riss()        
        if minBew > 0 or (Variable.stbkbKlaffPruef and Variable.stbobDruc[2] and Variable.stbobDruc[3] == False):
            Variable.stbobminBew = True
        else:
            Variable.stbobminBew = False
        
    elif Variable.stboNachweis == 2:
        Variable.stbobminBew = False

    Variable.stboii = ii

    if Variable.stboNachweis == 1:
        if Variable.stboii < 20:
            Variable.stbZiZ = 1
        else:
            Variable.stbZiZ = 2
    elif Variable.stboNachweis == 2:
        # design for the fracture state
        Variable.stbZiZ = 1
        # Reinforcement content is specified, is not calculated
        Variable.stbZmue0[0] = Variable.stbovormue0[0]
        Variable.stbZmue0[1] = Variable.stbovormue0[1]
        Variable.stbZmue0[2] = Variable.stbovormue0[2]
        # Initial values ​​are pre-assigned
        Variable.stbZgamC[1] = Variable.stbogamC[1]
        Variable.stbZgamS[1] = Variable.stbogamS[1]
        for i in range(0,4):
            Variable.stbZNucs[i] = 0
            Variable.stbZzi[i] = 0

        # Specifications for the shear force design (Anchorage and Shock)
        if Variable.stboNorm == 0:
            # Limits of shear stress and bond stresses
            if Variable.stbofck <= 15:
                Variable.stbotau012 = round(stbk15tau012 * Variable.stbofck / 15, 2)
                Variable.stbotau02 = round(stbk15tau02 * Variable.stbofck / 15, 2)
                Variable.stbotau03 = round(stbk15tau03 * Variable.stbofck / 15, 2)
                Variable.stbotau1 = round(stbk15tau1 * Variable.stbofck / 15, 2)
                Variable.stbotau2 = round(stbk15tau2 * Variable.stbofck / 15, 2)
            elif Variable.stbofck <= 25:
                Variable.stbotau012 = round(stbk15tau012 + (stbk25tau012 - stbk15tau012) * (Variable.stbofck - 15) / 10, 2)
                Variable.stbotau02 = round(stbk15tau02 + (stbk25tau02 - stbk15tau02) * (Variable.stbofck - 15) / 10, 2)
                Variable.stbotau03 = round(stbk15tau03 + (stbk25tau03 - stbk15tau03) * (Variable.stbofck - 15) / 10, 2)
                Variable.stbotau1 = round(stbk15tau1 + (stbk25tau1 - stbk15tau1) * (Variable.stbofck - 15) / 10, 2)
                Variable.stbotau2 = round(stbk15tau2 + (stbk25tau2 - stbk15tau2) * (Variable.stbofck - 15) / 10, 2)
            elif Variable.stbofck <= 35:
                Variable.stbotau012 = round(stbk25tau012 + (stbk35tau012 - stbk25tau012) * (Variable.stbofck - 25) / 10, 2)
                Variable.stbotau02 = round(stbk25tau02 + (stbk35tau02 - stbk25tau02) * (Variable.stbofck - 25) / 10, 2)
                Variable.stbotau03 = round(stbk25tau03 + (stbk35tau03 - stbk25tau03) * (Variable.stbofck - 25) / 10, 2)
                Variable.stbotau1 = round(stbk25tau1 + (stbk35tau1 - stbk25tau1) * (Variable.stbofck - 25) / 10, 2)
                Variable.stbotau2 = round(stbk25tau2 + (stbk35tau2 - stbk25tau2) * (Variable.stbofck - 25) / 10, 2)
            elif Variable.stbofck <= 45:
                Variable.stbotau012 = round(stbk35tau012 + (stbk45tau012 - stbk35tau012) * (Variable.stbofck - 35) / 10, 2)
                Variable.stbotau02 = round(stbk35tau02 + (stbk45tau02 - stbk35tau02) * (Variable.stbofck - 35) / 10, 2)
                Variable.stbotau03 = round(stbk35tau03 + (stbk45tau03 - stbk35tau03) * (Variable.stbofck - 35) / 10, 2)
                Variable.stbotau1 = round(stbk35tau1 + (stbk45tau1 - stbk35tau1) * (Variable.stbofck - 35) / 10, 2)
                Variable.stbotau2 = round(stbk35tau2 + (stbk45tau2 - stbk35tau2) * (Variable.stbofck - 35) / 10, 2)
            elif Variable.stbofck <= 55:
                Variable.stbotau012 = round(stbk45tau012 + (stbk55tau012 - stbk45tau012) * (Variable.stbofck - 45) / 10, 2)
                Variable.stbotau02 = round(stbk45tau02 + (stbk55tau02 - stbk45tau02) * (Variable.stbofck - 45) / 10, 2)
                Variable.stbotau03 = round(stbk45tau03 + (stbk55tau03 - stbk45tau03) * (Variable.stbofck - 45) / 10, 2)
                Variable.stbotau1 = round(stbk45tau1 + (stbk55tau1 - stbk45tau1) * (Variable.stbofck - 45) / 10, 2)
                Variable.stbotau2 = round(stbk45tau2 + (stbk55tau2 - stbk45tau2) * (Variable.stbofck - 45) / 10, 2)
            else:
                Variable.stbotau012 = stbk55tau012
                Variable.stbotau02 = stbk55tau02
                Variable.stbotau03 = stbk55tau03
                Variable.stbotau1 = stbk55tau1
                Variable.stbotau2 = stbk55tau2
            
            if TauP1 > stbkepse3:
                Variable.stbotau012 = TauP1
            
            if TauP2 > stbkepse3:
                Variable.stbotau02 = TauP2
            
            if TauP3 > stbkepse3:
                Variable.stbotau03 = TauP3
            
        elif Variable.stboNorm > 0:
            Variable.stbomaxcottheta = TauP3
       
    Variable.stbZeps_c[1] = 0
    Variable.stbZeps_c[2] = 0
    Variable.stbZeps_s[1] = 0
    Variable.stbZeps_s[2] = 0
    Variable.stbZeps_s[2] = 0
    SRechenWerteZ(2)

    # Initial Values are calculated (Check if there is any error with the values =-> stbZbFehler = True/False)
    if Variable.stboNorm < 0 or Variable.stboD < stbkepse5 or ((Variable.stboQuer == 1 or Variable.stboQuer == 2) and Variable.stboKR < stbkepse5) or (Variable.stboQuer == 3 and Variable.stboRB < stbkepse5) or Variable.stboD - Variable.stboH[1] - Variable.stboH[2] < -stbkepse5 or Variable.stbofck < stbkepse5 or Variable.stboalpha < stbkepse5 or Variable.stboepscy < stbkepse7 or Variable.stboepscu < Variable.stboepscy - stbkepse7 or Variable.stbofyk < stbkepse5 or Variable.stboftk < Variable.stbofyk - stbkepse5 or Variable.stboepssy < stbkepse7 or Variable.stboepssu < Variable.stboepssy - stbkepse7 or Variable.stbogamC[0] < stbkepse5 or Variable.stbogamC[1] < stbkepse5 or Variable.stbogamS[0] < stbkepse5 or Variable.stbogamS[1] < stbkepse5 or (Variable.stboNachweis == 2 and Variable.stbotau02 < Variable.stbotau012 - stbkepse7) or (Variable.stboNachweis == 2 and Variable.stbotau03 < Variable.stbotau02 - stbkepse7):
        Variable.stbZbFehler = True
    else:
        Variable.stbZbFehler = False                        #print(RechenWerte)
#------------------------------------------------------------------------------------------------------#

def SRechenWerteZ(InOut):

    # There are some routines that are performed for both the fracture state (stbZiZ = 1) and the usage state (stbZiZ = 2).
    # With the call SRechenWerteZ (1), depending on the value of the status flag, the relevant quantities are saved in the "neutral" calculation variables.
    # With the call SRechenWerteZ (2) at the end of the routine the values ​​of the "neutral" calculation variables can be saved back into the appropriate sizes.
    # There are some routines that are performed for both the fracture state (stbZiZ = 1) and the use state (stbZiZ = 2).
    # With the call SRechenWerteZ (1), depending on the value of the status flag, the relevant quantities are saved in the "neutral" calculation variables.
    # With the call SRechenWerteZ (2) at the end of the routine the values ​​of the "neutral" calculation variables can be saved back into the appropriate sizes.
    
    if InOut == 1:
        if Variable.stbZiZ == 1:
            Variable.stbZ_H[1] = Variable.stboH[1 + Variable.stboVMd]
            Variable.stbZ_H[2] = Variable.stboH[2 - Variable.stboVMd]
            Variable.stbZeps_c[1] = Variable.stbZepscd[1]
            Variable.stbZeps_c[2] = Variable.stbZepscd[2]
            Variable.stbZeps_s[1] = Variable.stbZepssd[1]
            Variable.stbZeps_s[2] = Variable.stbZepssd[2]
        elif Variable.stbZiZ == 2:
            Variable.stbZ_H[1] = Variable.stboH[1 + Variable.stboVMk]
            Variable.stbZ_H[2] = Variable.stboH[2 - Variable.stboVMk]
            Variable.stbZeps_c[1] = Variable.stbZepsck[1]
            Variable.stbZeps_c[2] = Variable.stbZepsck[2]
            Variable.stbZeps_s[1] = Variable.stbZepssk[1]
            Variable.stbZeps_s[2] = Variable.stbZepssk[2]
        
    elif InOut == 2:
        if Variable.stbZiZ == 1:
            Variable.stbZepscd[1] = Variable.stbZeps_c[1]
            Variable.stbZepscd[2] = Variable.stbZeps_c[2]
            Variable.stbZepssd[1] = Variable.stbZeps_s[1]
            Variable.stbZepssd[2] = Variable.stbZeps_s[2]
        elif Variable.stbZiZ == 2:
            Variable.stbZepsck[1] = Variable.stbZeps_c[1]
            Variable.stbZepsck[2] = Variable.stbZeps_c[2]
            Variable.stbZepssk[1] = Variable.stbZeps_s[1]
            Variable.stbZepssk[2] = Variable.stbZeps_s[2]                #print (SRechenWerteZ)
#------------------------------------------------------------------------------------------------------#

def SgamCSini(gam_c, gam_s, delt_S, delt_K):
    # Partial safety factors
    Variable.stbogamC[1] = gam_c / Variable.stboalpha
    if Variable.stboNorm == 0:
        Variable.stbogamC[0] = (gam_c + delt_S) / Variable.stboalpha
    elif Variable.stboNorm == 1:
        Variable.stbogamC[0] = (gam_c + delt_S) / Variable.stboalpha
    elif Variable.stboNorm == 2:
        Variable.stbogamC[0] = gam_c / (Variable.stboalpha - delt_S)
    elif Variable.stboNorm == 3:
        Variable.stbogamC[0] = gam_c / (Variable.stboalpha - delt_S)

    if Variable.stboNorm == 0:
        Variable.stbogamS[1] = gam_c
        Variable.stbogamS[0] = gam_c + delt_S
    elif Variable.stboNorm > 0:
        Variable.stbogamS[1] = gam_s
        Variable.stbogamS[0] = gam_s
    Smue0Druc(delt_S, delt_K)                                           #print(SgamCSini)
#------------------------------------------------------------------------------------------------------#

def stbfeBew():
    # Reinforcement Geometries Dimensionless
    SRechenWerteZ(1)
    if Variable.stboQuer == 3 and Variable.stbobHkrit == True:
        stbfeBew = (Variable.stbZ_H[2] - Variable.stbZ_H[1]) / 2 / Variable.stboD
    else:
        stbfeBew = 0
    return stbfeBew
#------------------------------------------------------------------------------------------------------#    

def Sdehnkrit():
    #Critical strain states are required for the iterative determination of the equilibrium states
    #Related or reduced internal forces
    f_null = [0,1,0,0]
    dehn = [0,0,0,0]
    SRechenWerteZ(1)
    for it_dehn in range (1,stbkitmax+1):
        if abs(f_null[1]) > stbkepse5:
            Sitdehn(dehn, f_null, it_dehn)
            Sdehnepscs(dehn[1])
            n_eU = stbfKneU()
            m_eU = stbfKmeU()
            f_null[1] = n_eU + m_eU
        else:
            break
    Variable.stbodehnkrit[0] = dehn[1]                                  #print(Sdehnkrit)
#------------------------------------------------------------------------------------------------------#

def Smue0Riss():
    # Determination of the minimum reinforcement stbomue0Riss () for the crack moment
    EingangWerte = [0 for i in range(0,10)]
    EingangWerte[0] = Variable.stboNd
    EingangWerte[1] = Variable.stboMd
    EingangWerte[2] = Variable.stbofyk
    EingangWerte[3] = Variable.stboftk
    EingangWerte[4] = Variable.stbovormue0[0]
    EingangWerte[5] = Variable.stbovormue0[1]
    EingangWerte[6] = Variable.stbovormue0[2]
    EingangWerte[7] = Variable.stbomue0Druc[0]
    EingangWerte[8] = Variable.stbomue0Druc[1]
    EingangWerte[9] = Variable.stbomue0Druc[2]

    #Fracture state
    Variable.stbZiZ = 1

    #Exploitation of concrete
    if Variable.stboNorm == 0:
        Variable.stbZgamC[1] = 1 / Variable.stboalpha
    elif Variable.stboNorm > 0:
        Variable.stbZgamC[1] = Variable.stbogamC[1]
    
    #Use of reinforcement
    Variable.stbZgamS[1] = 1

    ''' 
    For stboNorm = 0 becomes
    '   f_yk = 0.8 * stbofyk
    '   f_tk = 0.8 * stbofyk
    'otherwise
    '   f_yk = 1.0 * stbofyk
    '   f_tk = 1.0 * stbofyk
    'set
    '''
    
    if Variable.stboNorm == 0:
        Variable.stbofyk = 0.8 * Variable.stbofyk
        Variable.stboftk = Variable.stbofyk
    elif Variable.stboNorm > 0:
        Variable.stbofyk = Variable.stbofyk
        Variable.stboftk = Variable.stbofyk
    
    # Determination of stbomue0Riss ()
    Variable.stbovormue0[0] = Variable.stbovormue0[0] * Variable.stboftk / EingangWerte[3]
    Variable.stbovormue0[1] = Variable.stbovormue0[1] * Variable.stboftk / EingangWerte[3]
    Variable.stbovormue0[2] = Variable.stbovormue0[2] * Variable.stboftk / EingangWerte[3]
    Variable.stbomue0Druc[0] = Variable.stbomue0Druc[0] * Variable.stboftk / EingangWerte[3]
    Variable.stbomue0Druc[1] = Variable.stbomue0Druc[1] * Variable.stboftk / EingangWerte[3]
    Variable.stbomue0Druc[2] = Variable.stbomue0Druc[2] * Variable.stboftk / EingangWerte[3] 
    Variable.stboNd = 0
    Variable.stbomue0Riss[0] = 0
    Variable.stbomue0Riss[1] = 0
    Variable.stbomue0Riss[2] = 0
    Variable.stboMd = math.pi * stbffctm() / Variable.stbofck / 6
    Serfmue0_K()
    Variable.stbZerfmue0[1] = 0
    Variable.stbZerfmue0[2] = 0   
    Variable.stbomue0Riss[0] = Variable.stbZerfmue0[0] * EingangWerte[3] / Variable.stboftk
    Variable.stbomue0Riss[1] = Variable.stbZerfmue0[1] * EingangWerte[3] / Variable.stboftk
    Variable.stbomue0Riss[2] = Variable.stbZerfmue0[2] * EingangWerte[3] / Variable.stboftk
    Variable.stboNd = EingangWerte[0]
    Variable.stboMd = EingangWerte[1]
    Variable.stbofyk = EingangWerte[2]
    Variable.stboftk = EingangWerte[3]
    Variable.stbovormue0[0] = EingangWerte[4]
    Variable.stbovormue0[1] = EingangWerte[5]
    Variable.stbovormue0[2] = EingangWerte[6]
    Variable.stbomue0Druc[0] = EingangWerte[7]
    Variable.stbomue0Druc[1] = EingangWerte[8]
    Variable.stbomue0Druc[2] = EingangWerte[9]                                  #print(Smue0Riss)
#------------------------------------------------------------------------------------------------------#

def Smue0Druc(delt_S, delt_K):
    # For stboNorm = 0
    # Strain limits for the reinforcement of the train side to increase the safety factor
    # otherwise
    # Minimum reinforcement content for pressure-loaded components to increase the partial safety factor for concrete determined
   
    NEdmin = 0
    mue0min = 0
    StrVek = delt_K.split(" ")
    StrVek[0] = float(StrVek[0])
    StrVek[1] = float(StrVek[1])

    if Variable.stboNorm == 0:
        Variable.stboepsSmin[1] = StrVek[0]/ 1000
        if StrVek[1] == StrVek[0]:
            Variable.stboepsSmin[2] = 0
        else:
            Variable.stboepsSmin[2] = (StrVek[0]+1)/ 1000
        Variable.stbomue0Druc[0] = 0
        Variable.stbomue0Druc[1] = 0
        Variable.stbomue0Druc[2] = 0

    elif Variable.stboNorm > 0:
        if Variable.stbobDruc[1]:
            if Variable.stboNorm == 2:
                NEdmin = StrVek[0]
                if StrVek[1] == StrVek[0]:
                    mue0min = 0.002 * Variable.stboftk / Variable.stbofck
                else:
                    mue0min = max((StrVek[0] + 1) / 100, 0) * Variable.stboftk / Variable.stbofck
                
                if Variable.stboQuer == 1 or Variable.stboQuer == 2:
                    Variable.stbomue0Druc[0] = max(NEdmin * abs(Variable.stboNd) * Variable.stbogamS[1] / math.pi * Variable.stboftk / Variable.stbofyk, mue0min)
                    Variable.stbomue0Druc[1] = 0
                    Variable.stbomue0Druc[2] = 0
            else:
                NEdmin = StrVek[0]
                if Variable.stboQuer == 1 or Variable.stboQuer == 2:
                    Variable.stbomue0Druc[0] = NEdmin * abs(Variable.stboNd) * Variable.stbogamS[1] / math.pi * Variable.stboftk / Variable.stbofyk
                    Variable.stbomue0Druc[1] = 0
                    Variable.stbomue0Druc[2] = 0
        else:     
            Variable.stbomue0Druc[0] = 0
            Variable.stbomue0Druc[1] = 0
            Variable.stbomue0Druc[2] = 0                                #print(Smue0Druc)
#------------------------------------------------------------------------------------------------------#

def Sitdehn(dehn, f_null, it_dehn):
    # Iteration procedure to determine the state of elongation at break

    # The fracture-elongation states are measured with the variable "dehn"
    # described. "dehn" can take values ​​from the interval [-1, +1]
    # The values ​​have the following meaning:
    '''
    # dehn      stbZepscd [1]   stbZepssd [1]   stbZepscd [2]

    # -1.0      -stboepscy      -stboepscy
    # -0.5      -stboepscu                      0.0
    # 0.0       -stboepscu      + stboeps_su
    # +1.0      + stboeps_su    + stboeps_su

    # '''
    # For intermediate values ​​of "dehn", the steel or concrete strain is interpolated linearly.
    # In the first two steps, the fractional internal forces
    # calculated for the outer interval limits of the variable dehn.
    # Then the interval size is continuously halved,
    # where the new interval by comparing the signs of the
    # Zero function f_Null is determined.
    if it_dehn == 1:
        f_null[1] = 0
        dehn[1] = -1
    elif it_dehn == 2:
        dehn[2] = dehn[1]
        f_null[2] = f_null[1]
        dehn[1] = 1
    elif it_dehn == 3:
        dehn[3] = dehn[1]
        f_null[3] = f_null[1]
        dehn[1] = (dehn[2] + dehn[3]) / 2
    else:
        if Variable.Nd1 < -stbkepse3:
            if f_null[1] * f_null[2] < 0:
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
            else:
                dehn[2] = dehn[1]
                f_null[2] = f_null[1]
            
        else:
            if f_null[1] * f_null[3] < 0:
                #print("at1")
                dehn[2] = dehn[1]
                f_null[2] = f_null[1]
            else:
                #print("at2")
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
        dehn[1] = (dehn[2] + dehn[3]) / 2                               #print(Sitdehn)
#------------------------------------------------------------------------------------------------------#

def Sdehnepscs(dehn):
    # Calculates the concrete and steel strain for a specific value of the variable "dehn"
    SRechenWerteZ(1)

    # Calculates the concrete strain stbZepscd (1) for a certain value of the variable "dehn".
    if dehn < -0.5:
        Variable.stbZeps_c[1] = -Variable.stboepscu + (Variable.stboepscu - Variable.stboepscy) * (-0.5 - dehn) / 0.5
    elif dehn < 0:
        Variable.stbZeps_c[1] = -Variable.stboepscu
    else:
        Variable.stbZeps_c[1] = -Variable.stboepscu + dehn * (Variable.stboepscu + Variable.stboepssu)
    
    # Calculates the steel strain stbZepssd (1) for a certain value of the variable "dehn".
    if dehn < -0.5:
        eps_gr = -Variable.stboepscu * Variable.stbZ_H[1] / Variable.stboD
        Variable.stbZeps_s[1] = eps_gr + (Variable.stboepscy + eps_gr) * (dehn + 0.5) / 0.5
    elif dehn < 0:
        eps_gr = -Variable.stboepscu * Variable.stbZ_H[1] / Variable.stboD
        Variable.stbZeps_s[1] = Variable.stboepssu + (Variable.stboepssu - eps_gr) * dehn / 0.5
    else:
        Variable.stbZeps_s[1] = Variable.stboepssu

    SRechenWerteZ(2)
    # Sepsc2s2 Calculates the strains stbZepscd (2) and stbZepssd (2)
    Sepsc2s2()
#------------------------------------------------------------------------------------------------------#

def Sepsc2s2():
    # Calculates the strains stbZepscd (2) and stbZepssd (2)
    SRechenWerteZ(1)
    
    Variable.stbZeps_c[2] = Variable.stbZeps_c[1] + (Variable.stbZeps_s[1] - Variable.stbZeps_c[1]) * Variable.stboD / (Variable.stboD - Variable.stbZ_H[1])
    Variable.stbZeps_s[2] = Variable.stbZeps_c[1] + (Variable.stbZeps_s[1] - Variable.stbZeps_c[1]) * Variable.stbZ_H[2] / (Variable.stboD - Variable.stbZ_H[1])
    
    SRechenWerteZ(2)
#------------------------------------------------------------------------------------------------------#


def stbffctm():
    # Tensile strength of the concrete
    if Variable.stboNorm == 0:
        stbffctm = 0.25 * max(Variable.stbofck, 35) ** (2 / 3)
    elif Variable.stboNorm > 0:
        if Variable.stbofck < 52.5:
            stbffctm = 0.3 * Variable.stbofck ** (2 / 3)
        else:
            stbffctm = 2.12 * math.log(1 + (Variable.stbofck + 8) / 10)
    return stbffctm
#------------------------------------------------------------------------------------------------------#    

def SRissB():
    # Design taking into account the crack width limitation.
    # statically required reinforcement stbZerfmue0 and associated safety factors stbZgamC (1), stbZgamS (1)
    # Information on minimum reinforcement is also taken into account.
    SgamC1()

    if Variable.stboRissP1 >= 1 or Variable.stboii >= 20:
        #Condition of use
        #The characteristic internal forces stbZRNk, stbZRMk and the associated elongation state stbZepsck, stbZepssk are determined.
        #Characteristic state
        #The characteristic internal forces stbZRNk, stbZRMk and the associated strain state stbZepsck, stbZepssk are determined.
        Gebrauch_K()

    if Variable.stboRissP1 >= 1 and stbfsig_s(Variable.stbZepssk[1]) > Variable.stboRissP1:
        # Determination of the required reinforcement content for a given steel stress / strain
        # Determination of the required reinforcement content for a given steel tension / steel elongation
        # If stboRissP1> = 1 # And stbfsig_s (stbZepssk (1))> stboRissP1 Then
        SigVor_K()

    if Variable.stboQuer == 1 and Variable.stbZmue0[0] > Variable.stbZerfmue0[0] + stbkepse5:
        # Elongation at break
        #The fracture internal forces stbZRNd, stbZRMd and the elongation state stbZepscd, stbZepssd are determined.
        #Elongation state
        #The fracture intersection sizes stbZRNd, stbZRMd and the strain state stbZepscd, stbZepssd are determined.
        Bruch_K()
#------------------------------------------------------------------------------------------------------#

def SgamC1():
    # The safety factors stbZgamC [1], stbZgamS [1] are determined iteratively
    # The corresponding statically required reinforcement is determined.
    # Auxiliary quantities
    fnullC = [0,0,0,0]

    Variable.stbZiZ = 1
    SRechenWerteZ(1)

    # Specified reinforcement
    if Variable.stbobminBew :
        vormue0_3 = max(Variable.stbovormue0[0], Variable.stbomue0Riss[0]) + max(Variable.stbovormue0[1], Variable.stbomue0Riss[1]) + max(Variable.stbovormue0[2], Variable.stbomue0Riss[2])
    else:
        vormue0_3 = Variable.stbovormue0[0] + Variable.stbovormue0[1] + Variable.stbovormue0[2]
    
    # If stbobDruc [1] = True and (stboNorm = 0 or stbomue0Druc [0] + stbomue0Druc [1] + stbomue0Druc [1] - vormue0_3> stbkepse7 or stbobHkrit = True) applies,
    # the value of stbZgamC [1] must be iterated from stbogamC [0] (increased security level),
    # to guarantee continuity of the solution and thus convergence
    if Variable.stbobDruc[1] and (Variable.stboNorm == 0 or Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2] - vormue0_3 > stbkepse7 or Variable.stbobHkrit) :
        Variable.stbZgamC[1] = Variable.stbogamC[0]
        Variable.stbZgamS[1] = Variable.stbogamS[0]
        bLastLoop = False
    else:
        Variable.stbZgamC[1] = Variable.stbogamC[1]
        Variable.stbZgamS[1] = Variable.stbogamS[1]
        bLastLoop = True
    
    bLoop = True
    it_gamC = 1
    # Determination of the required reinforcement contents stbZerfmue0 [0]
    if Variable.stboQuer == 1 :
        Serfmue0_K()
        erfmue_0 = Variable.stbZerfmue0[0]

    # Maximum from required reinforcement and reinforcement specifications
    if Variable.stboQuer == 1 :
        Variable.stbZmue0[0] = max(Variable.stbZerfmue0[0], Variable.stbovormue0[0])
        Variable.stbZmue0[1] = 0
        Variable.stbZmue0[2] = 0
        
    if bLastLoop :
        bLoop = False
    else:
        if Variable.stboNorm == 0 :
            if erfmue_0 < stbkepse7 :
                interpol = 0
            else:
                # The correct elongation at break must be known for the interpolation.
                if Variable.stboQuer == 1 and Variable.stbZmue0[0] > Variable.stbZerfmue0[0] + stbkepse5 :
                    Bruch_K()
                interpol = max((Variable.stbZepssd[1] - Variable.stboepsSmin[2]) / (Variable.stboepsSmin[1] - Variable.stboepsSmin[2]), 0)
            
        else:
            interpol = (Variable.stbZmue0[0] + Variable.stbZmue0[1] + Variable.stbZmue0[2]) / (Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2])
        
        fnullC[1] = Variable.stbZgamC[1] - Variable.stbogamC[0] + (Variable.stbogamC[0] - Variable.stbogamC[1]) * interpol
        if it_gamC == 1 :
            if interpol > stbkepse5 :
                fnullC[3] = fnullC[1]
                Variable.stbZgamC[3] = Variable.stbZgamC[1]
                Variable.stbZgamC[1] = Variable.stbogamC[1]
                Variable.stbZgamS[3] = Variable.stbZgamS[1]
                Variable.stbZgamS[1] = Variable.stbogamS[1]
            else:
                bLoop = False
            
        elif it_gamC == 2 :
            if interpol < 1 - stbkepse5 :
                fnullC[2] = fnullC[1]
                Variable.stbZgamC[2] = Variable.stbZgamC[1]
                Variable.stbZgamC[1] = (Variable.stbZgamC[2] + Variable.stbZgamC[3]) / 2
                Variable.stbZgamS[2] = Variable.stbZgamS[1]
                Variable.stbZgamS[1] = (Variable.stbZgamS[2] + Variable.stbZgamS[3]) / 2
            else:
                bLoop = False
            
        else:
            if fnullC[1] * fnullC[2] < 0 :
                Variable.stbZgamC[3] = Variable.stbZgamC[1]
                Variable.stbZgamS[3] = Variable.stbZgamS[1]
                fnullC[3] = fnullC[1]
            else:
                Variable.stbZgamC[2] = Variable.stbZgamC[1]
                Variable.stbZgamS[2] = Variable.stbZgamS[1]
                fnullC[2] = fnullC[1]
            
            Variable.stbZgamC[1] = (Variable.stbZgamC[2] + Variable.stbZgamC[3]) / 2
            Variable.stbZgamS[1] = (Variable.stbZgamS[2] + Variable.stbZgamS[3]) / 2
            if Variable.stbZgamC[3] - Variable.stbZgamC[2] < stbkepse3 :
                bLastLoop = True
                if Variable.stbobHkrit :
                    Variable.stbZgamC[1] = Variable.stbZgamC[3]
                    Variable.stbZgamS[1] = Variable.stbZgamS[3]
    while bLoop and it_gamC < stbkitmax:

        it_gamC = it_gamC + 1
        # Determination of the required reinforcement contents stbZerfmue0 [0]
        if Variable.stboQuer == 1 :
            Serfmue0_K()
            erfmue_0 = Variable.stbZerfmue0[0]
        
        if Variable.stboQuer == 1 :
            Variable.stbZmue0[0] = max(Variable.stbZerfmue0[0], Variable.stbovormue0[0])
            Variable.stbZmue0[1] = 0
            Variable.stbZmue0[2] = 0
            
        # Maximum from required reinforcement and reinforcement specifications
        if bLastLoop :
            bLoop = False
        else:
            if Variable.stboNorm == 0 :
                if erfmue_0 < stbkepse7 :
                    interpol = 0
                else:
                    # The correct elongation at break must be known for the interpolation.
                    if Variable.stboQuer == 1 and Variable.stbZmue0[0] > Variable.stbZerfmue0[0] + stbkepse5 :
                        Bruch_K()
                    interpol = max((Variable.stbZepssd[1] - Variable.stboepsSmin[2]) / (Variable.stboepsSmin[1] - Variable.stboepsSmin[2]), 0)
                
            else:
                interpol = (Variable.stbZmue0[0] + Variable.stbZmue0[1] + Variable.stbZmue0[2]) / (Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2])
            
            fnullC[1] = Variable.stbZgamC[1] - Variable.stbogamC[0] + (Variable.stbogamC[0] - Variable.stbogamC[1]) * interpol
            if it_gamC == 1 :
                if interpol > stbkepse5 :
                    fnullC[3] = fnullC[1]
                    Variable.stbZgamC[3] = Variable.stbZgamC[1]
                    Variable.stbZgamC[1] = Variable.stbogamC[1]
                    Variable.stbZgamS[3] = Variable.stbZgamS[1]
                    Variable.stbZgamS[1] = Variable.stbogamS[1]
                else:
                    bLoop = False
                
            elif it_gamC == 2 :
                if interpol < 1 - stbkepse5 :
                    fnullC[2] = fnullC[1]
                    Variable.stbZgamC[2] = Variable.stbZgamC[1]
                    Variable.stbZgamC[1] = (Variable.stbZgamC[2] + Variable.stbZgamC[3]) / 2
                    Variable.stbZgamS[2] = Variable.stbZgamS[1]
                    Variable.stbZgamS[1] = (Variable.stbZgamS[2] + Variable.stbZgamS[3]) / 2
                else:
                    bLoop = False
                
            else:
                if fnullC[1] * fnullC[2] < 0 :
                    Variable.stbZgamC[3] = Variable.stbZgamC[1]
                    Variable.stbZgamS[3] = Variable.stbZgamS[1]
                    fnullC[3] = fnullC[1]
                else:
                    Variable.stbZgamC[2] = Variable.stbZgamC[1]
                    Variable.stbZgamS[2] = Variable.stbZgamS[1]
                    fnullC[2] = fnullC[1]
                
                Variable.stbZgamC[1] = (Variable.stbZgamC[2] + Variable.stbZgamC[3]) / 2
                Variable.stbZgamS[1] = (Variable.stbZgamS[2] + Variable.stbZgamS[3]) / 2
                if Variable.stbZgamC[3] - Variable.stbZgamC[2] < stbkepse3 :
                    bLastLoop = True
                    if Variable.stbobHkrit :
                        Variable.stbZgamC[1] = Variable.stbZgamC[3]
                        Variable.stbZgamS[1] = Variable.stbZgamS[3]

    if it_gamC == stbkitmax :
        print(" Error in sgamc1")
        Variable.stbZbFehler = True
#------------------------------------------------------------------------------------------------------#

def Sitdehn0(dehn, f_null, it_dehn):
    # Iteration process for the unreinforced cross section
    if it_dehn == 1:
        f_null[1] = 0
        dehn[1] = -1
    elif it_dehn == 2:
        dehn[2] = dehn[1]
        f_null[2] = f_null[1]
        # Expansion state with the maximum possible load center for the unreinforced cross-section
        # stbZepscd (1) = very small negative value
        # stbZepssd (1) = stboepssu
        dehn[1] = Variable.stboepscu / (Variable.stboepscu + Variable.stboepssu) - stbkepse5
    elif it_dehn == 3:
        dehn[3] = dehn[1]
        f_null[3] = f_null[1]
        dehn[1] = (dehn[2] + dehn[3]) / 2
    else:
        if f_null[1] * f_null[2] < 0:
            dehn[3] = dehn[1]
            f_null[3] = f_null[1]
        else:
            dehn[2] = dehn[1]
            f_null[2] = f_null[1]
        
        dehn[1] = (dehn[2] + dehn[3]) / 2                                               #print(Sitdehn0)
#------------------------------------------------------------------------------------------------------#

def stbfalpha():
    # Determines the iteratively adjusted reduction value alpha
    if Variable.stboNorm == 0 or Variable.stboNorm == 1:
        stbfalpha = Variable.stboalpha
    elif Variable.stboNorm == 2 or Variable.stboNorm == 3:
        stbfalpha = Variable.stboalpha * Variable.stbogamC[1] / Variable.stbZgamC[1]
    return stbfalpha
#------------------------------------------------------------------------------------------------------#

def stbfsig_s(eps_s):
    # Calculates the steel stress depending on the steel strain "eps_s".
    if abs(eps_s) <= Variable.stboepssy:
        stbfsig_s = eps_s / Variable.stboepssy * Variable.stbofyk
    elif abs(eps_s) <= Variable.stboepssu:
        stbfsig_s = math.copysign(1,eps_s) * (Variable.stbofyk + (Variable.stboftk - Variable.stbofyk) * (abs(eps_s) - Variable.stboepssy) / (Variable.stboepssu - Variable.stboepssy))
    else:
        stbfsig_s = math.copysign(1,eps_s) * Variable.stboftk
    return stbfsig_s
#------------------------------------------------------------------------------------------------------#
#############################----Circular Cross-Sectional Specification----#############################
# Constants
i2n = 9
# Numerical integration according to the Simpson rule: number of support points = 2 * i2n + 1
# with i2n = 5 the convergence in function Snue0_K is extremely slow with an internal force combination for which dehn (1) = -0.5 applies
#------------------------------------------------------------------------------------------------------#
def Serfmue0_K():
    # Related or reduced internal forces
    dehn = [0,0,0,0]
    f_null = [0,1,0,0]

    # Iteration procedure to determine the statically required reinforcement stbZerfmue0[0]
    for it_dehn in range(1,stbkitmax):
        if (it_dehn==1 and (Variable.stboNd >= stbkepse5 or Variable.stboMd >= stbkepse5))or((it_dehn == 2 and (Variable.stboNd <= -stbkepse5 or Variable.stboMd >= stbkepse5)) or it_dehn == 3 or abs(f_null[1]) > stbkepse7):
            # The dehn (elongation) at break for the next step is determined
            if it_dehn == 3 :
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
                dehn[1] = Variable.stbodehnkrit[0]
            else:
                Sitdehn(dehn, f_null, it_dehn)
            # Concrete and steel expansions
            Sdehnepscs(dehn[1])

            # Related internal forces of the concrete pressure zone
            n_bU = stbfKnbU()
            m_bU = stbfKmbU()

            # Reduced internal forces of the reinforcement ring
            n_eU = stbfKneU()
            m_eU = stbfKmeU()

            if abs(n_eU + m_eU) > stbkepse5 :
                Variable.stbZerfmue0[0] = Variable.stbZgamS[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] + Variable.stboMd - m_bU / Variable.stbZgamC[1]) / (n_eU + m_eU)
            else:
                Variable.stbZerfmue0[0] = 1 / stbkepse7
            
            # Function whose zero point is Desired
            f_null[1] = m_eU * (Variable.stboNd - n_bU / Variable.stbZgamC[1]) - n_eU * (Variable.stboMd - m_bU / Variable.stbZgamC[1])
            # The optimization function Sub Smue0opt converges more evenly.
            # (otherwise erratic change between symmetrical and non-symmetrical reinforcement with little change in the center)
        
        else:
            break

    if it_dehn == stbkitmax : 
        print('error = ',Variable.stbZbFehler)

    # Check minimum reinforcement and determine fracture internal forces
    if Variable.stbobminBew ==  True and Variable.stbZerfmue0[0] < Variable.stbomue0Riss[0] :
        Variable.stbZerfmue0[0] = Variable.stbomue0Riss[0]
        Variable.stbZmue0[0] = Variable.stbZerfmue0[0]
        Bruch_K()
    else:
        Variable.stbZRNd = n_bU / Variable.stbZgamC[1] + Variable.stbZerfmue0[0] * n_eU / Variable.stbZgamS[1]
        Variable.stbZRMd = m_bU / Variable.stbZgamC[1] + Variable.stbZerfmue0[0] * m_eU / Variable.stbZgamS[1]                              #print(Serfmue0_K)
#------------------------------------------------------------------------------------------------------#

def stbfphiAo():
    # Angle required for numerical integration calculations 
    # Split in conditions due to arc tan
    SRechenWerteZ(1)
    r1 = 1

    # Determined by using stbZeps_c[1] and stbZeps_c[2]
    if Variable.stbZeps_c[1] < 0 :
        if Variable.stbZeps_c[2] < 0 or abs(Variable.stbZeps_c[1] - Variable.stbZeps_c[2]) < stbkepse7 :
            stbfphiAo = math.pi
        else:
            x = 2 * r1 * Variable.stbZeps_c[1] / (Variable.stbZeps_c[1] - Variable.stbZeps_c[2])
            q = (r1 - x) / r1
            if math.sqrt(1 - q ** 2) == 0:
                stbfphiAo = math.pi / 2 - math.copysign(1,q)*(math.pi / 2)
            else:
                stbfphiAo = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
    
    else:
        stbfphiAo = 0

    return stbfphiAo
#------------------------------------------------------------------------------------------------------#

def stbfphiAu():
    # Angle required for numerical integration calculations.
    SRechenWerteZ(1)
    r1 = 1

    # Determined by using stbZeps_c[1] and stbZeps_c[2]
    if Variable.stbZeps_c[1] < -Variable.stboepscy :
        if abs(Variable.stbZeps_c[1] - Variable.stbZeps_c[2]) < stbkepse7 :
            stbfphiAu = math.pi
        else:
            xgr = 2 * r1 * (Variable.stbZeps_c[1] + Variable.stboepscy) / (Variable.stbZeps_c[1] - Variable.stbZeps_c[2])
            q = (r1 - xgr) / r1
            stbfphiAu = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
    
    else:
        stbfphiAu = 0

    return stbfphiAu
#------------------------------------------------------------------------------------------------------#

def stbfKnbU():
    # Integration limits, integration variable, delta_value
    # Related or reduced internal forces
    SRechenWerteZ(1)
    # Integration limits for the concrete cross section
    phiAo = stbfphiAo()
    phiAu = stbfphiAu()
    phiBo = phiAu
    phiBu = 0

    # Related internal forces of the concrete pressure zone
    if Variable.stbZeps_c[1] < 0 :
        k1 = -(Variable.stbZeps_c[1] + Variable.stbZeps_c[2]) / Variable.stboepscy / 2
        k2 = -(Variable.stbZeps_c[1] - Variable.stbZeps_c[2]) / Variable.stboepscy / 2
        if abs(phiAo - phiAu) < stbkepse7 :
            nAbU = 0
        elif abs(k2) < stbkepse7 :
            if k1 <= 0 :
                nAbU = 0
            elif k1 >= 1 :
                nAbU = -math.pi
            else:
                nAbU = -math.pi * (1 - (1 - k1) ** Variable.stbon2)

        else:
            nAbU = 0
            dphi = (phiAo - phiAu) / i2n
            phi = phiAu
            nAbU = nAbU + (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2
            phi = phiAo
            nAbU = nAbU + (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2
            phi = phiAu - dphi / 2
            for i in range(0 , i2n):
                phi = phi + dphi
                nAbU = nAbU + 4 * (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2
            phi = phiAu
            for i in range( 0, i2n-1):
                phi = phi + dphi
                nAbU = nAbU + 2 * (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2
            nAbU = nAbU * dphi / 3
        nBbU = -phiBo + math.sin(2 * phiBo) / 2 + phiBu - math.sin(2 * phiBu) / 2
    
    else:
        nAbU = 0
        nBbU = 0
    stbfKnbU = nAbU + nBbU
    
    return stbfKnbU
#------------------------------------------------------------------------------------------------------#

def stbfKmbU():
    # Integration limits, integration variable, delta_value
    # Related or reduced internal forces
    SRechenWerteZ(1)
    # Integration limits for the concrete cross section
    phiAo = stbfphiAo()
    phiAu = stbfphiAu()
    phiBo = phiAu
    phiBu = 0

    # Related internal forces of the concrete pressure zone
    if Variable.stbZeps_c[1] < 0 :
        k1 = -(Variable.stbZeps_c[1] + Variable.stbZeps_c[2]) / Variable.stboepscy / 2
        k2 = -(Variable.stbZeps_c[1] - Variable.stbZeps_c[2]) / Variable.stboepscy / 2
        if abs(phiAo - phiAu) < stbkepse7 :
            mAbU = 0
        elif abs(k2) < stbkepse7 :
            mAbU = 0
        else:
            mAbU = 0
            dphi = (phiAo - phiAu) / i2n
            phi = phiAu
            mAbU = mAbU + (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2 * math.cos(phi)
            phi = phiAo
            mAbU = mAbU + (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2 * math.cos(phi)
            phi = phiAu - dphi / 2
            for i in range(0 , i2n):
                phi = phi + dphi
                mAbU = mAbU + 4 * (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2 * math.cos(phi)
            phi = phiAu
            for i in range(0 , i2n-1):
                phi = phi + dphi
                mAbU = mAbU + 2 * (abs(k1 + k2 * math.cos(phi) - 1) ** Variable.stbon2 - 1) * math.sin(phi) ** 2 * math.cos(phi)
            mAbU = -mAbU * dphi / 3
        mBbU = 2 / 3 * (math.sin(phiBo) ** 3 - math.sin(phiBu) ** 3) #
    
    else:
        mAbU = 0
        mBbU = 0
    stbfKmbU = mAbU + mBbU
    
    return stbfKmbU
#------------------------------------------------------------------------------------------------------#

def stbfphiEu():
    # Angle required for numerical integration calculations
    SRechenWerteZ(1)
    R_e1 = 1

    # Determined by using stbZeps_c[1] and stbZeps_c[2]
    if Variable.stbZeps_s[1] > 0 + stbkepse7 :
        if Variable.stbZeps_s[2] < 0 - stbkepse7 :
            if Variable.stbZeps_s[2] < -Variable.stboepssy - stbkepse7 :
                xgr = 2 * R_e1 * (Variable.stbZeps_s[2] + Variable.stboepssy) / (Variable.stbZeps_s[2] - Variable.stbZeps_s[1])
                q = (R_e1 - xgr) / R_e1
                stbfphiEu = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
            else:
                stbfphiEu = 0

        else:
            stbfphiEu = 0
    else:
        if Variable.stbZeps_s[2] < -Variable.stboepssy - stbkepse7 :
            if Variable.stbZeps_s[1] > -Variable.stboepssy + stbkepse7 :
                xgr = 2 * R_e1 * (Variable.stbZeps_s[2] + Variable.stboepssy) / (Variable.stbZeps_s[2] - Variable.stbZeps_s[1])
                q = (R_e1 - xgr) / R_e1
                stbfphiEu = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
            else:
                stbfphiEu = math.pi

        else:
            stbfphiEu = 0
    
    return stbfphiEu
#------------------------------------------------------------------------------------------------------#

def stbfphiEo():
    # Angle required for numerical integration calculations
    SRechenWerteZ(1)
    R_e1 = 1

    # Determined by using stbZeps_c[1] and stbZeps_c[2]
    if Variable.stbZeps_s[1] > stbkepse7 :
        if Variable.stbZeps_s[2] < -stbkepse7 :
            if Variable.stbZeps_s[1] > Variable.stboepssy + stbkepse7 :
                xgr = 2 * R_e1 * (Variable.stbZeps_s[2] - Variable.stboepssy) / (Variable.stbZeps_s[2] - Variable.stbZeps_s[1])
                q = (R_e1 - xgr) / R_e1
                stbfphiEo = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
            else:
                stbfphiEo = math.pi

        else:
            if Variable.stbZeps_s[2] < Variable.stboepssy - stbkepse7 :
                if Variable.stbZeps_s[1] > Variable.stboepssy + stbkepse7 :
                    xgr = 2 * R_e1 * (Variable.stbZeps_s[2] - Variable.stboepssy) / (Variable.stbZeps_s[2] - Variable.stbZeps_s[1])
                    q = (R_e1 - xgr) / R_e1
                    stbfphiEo = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
                else:
                    stbfphiEo = math.pi
    
            else:
                stbfphiEo = 0

    else:
        stbfphiEo = math.pi
    
    return stbfphiEo
#------------------------------------------------------------------------------------------------------#

def stbfKneU():
    # Integration limits, integration variable, delta_value
    # Related or reduced internal forces
    SRechenWerteZ(1)

    # Integration limits for the reinforcement ring
    phiEu = stbfphiEu()
    phiEo = stbfphiEo()

    # Elastic Range
    k1 = (Variable.stbZeps_s[1] + Variable.stbZeps_s[2]) / Variable.stboepssy / 2
    k2 = (Variable.stbZeps_s[1] - Variable.stbZeps_s[2]) / Variable.stboepssy / 2

    #Plastic Range
    phi_u = phiEu
    phi_o = phiEo
    n_EeU = (k1 * phi_o - k2 * math.sin(phi_o)) - (k1 * phi_u - k2 * math.sin(phi_u))
    k1 = (Variable.stbZeps_s[1] + Variable.stbZeps_s[2]) / (Variable.stboepssu - Variable.stboepssy) / 2
    k2 = (Variable.stbZeps_s[1] - Variable.stbZeps_s[2]) / (Variable.stboepssu - Variable.stboepssy) / 2

    #Pressure Zone
    phi_u = 0
    phi_o = phiEu
    n_PaU = (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_o - k2 * math.sin(phi_o)) * (Variable.stboftk / Variable.stbofyk - 1) - phi_o) - (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_u - k2 * math.sin(phi_u)) * (Variable.stboftk / Variable.stbofyk - 1) - phi_u)
    
    #drawn zone
    phi_u = phiEo
    phi_o = math.pi
    n_PbU = (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_o - k2 * math.sin(phi_o)) * (Variable.stboftk / Variable.stbofyk - 1) + phi_o)- (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_u - k2 * math.sin(phi_u)) * (Variable.stboftk / Variable.stbofyk - 1) + phi_u)
    
    #reduced cutting size
    stbfKneU = (n_EeU + n_PaU + n_PbU) * Variable.stbofyk / Variable.stboftk
   
    return stbfKneU
#------------------------------------------------------------------------------------------------------#

def stbfKmeU():
    # Integration limits, integration variable, delta_value
    # Related or reduced internal forces
    SRechenWerteZ(1)

    # Integration limits for the reinforcement ring
    phiEu = stbfphiEu()
    phiEo = stbfphiEo()

    # Elastic Range
    k1 = (Variable.stbZeps_s[1] + Variable.stbZeps_s[2]) / Variable.stboepssy / 2
    k2 = (Variable.stbZeps_s[1] - Variable.stbZeps_s[2]) / Variable.stboepssy / 2

    #Plastic Range
    phi_u = phiEu
    phi_o = phiEo
    m_EeU = (k1 * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2))- (k1 * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2))
    k1 = (Variable.stbZeps_s[1] + Variable.stbZeps_s[2]) / (Variable.stboepssu - Variable.stboepssy) / 2
    k2 = (Variable.stbZeps_s[1] - Variable.stbZeps_s[2]) / (Variable.stboepssu - Variable.stboepssy) / 2
    
    #Pressure Zone
    phi_u = 0
    phi_o = phiEu
    m_PaU = (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) - math.sin(phi_o))- (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) - math.sin(phi_u))   
    
    #Drawn Zone
    phi_u = phiEo
    phi_o = math.pi
    m_PbU = (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) + math.sin(phi_o))- (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) + math.sin(phi_u))
    
    #reduced cutting size
    stbfKmeU = -Variable.stboRe / Variable.stboKR * (m_EeU + m_PaU + m_PbU) * Variable.stbofyk / Variable.stboftk
    
    return stbfKmeU
#------------------------------------------------------------------------------------------------------#

def Bruch_K():
    # Related or reduced internal forces
    dehn = [0,0,0,0]
    f_null = [0,0,0,0]

    Variable.stbZiZ = 1

    if abs(Variable.stboeNd) < stbkepse7 :
        if Variable.stboNd < 0 :
            itmin = 0
        else:
            itmin = 1
    else:
        itmin = 2

    # Strain state with maximum possible load center for the unreinforced cross-section
    # stbZepscd (1) = very small negative value
    # stbZepssd (1) = stboepssu
    dehnkrit = Variable.stboepscu / (Variable.stboepscu + Variable.stboepssu) - stbkepse5

    it_dehn = 1
    # Elongation at break for the next step is determined
    Sitdehn(dehn, f_null, it_dehn)
    # Concrete and steel expansions
    Sdehnepscs(dehn[1])
    n_bU = stbfKnbU()
    m_bU = stbfKmbU()
    n_i = n_bU / Variable.stbZgamC[1]
    m_i = m_bU / Variable.stbZgamC[1]
    n_eU = stbfKneU()
    m_eU = stbfKmeU()
    n_i = n_i + Variable.stbZmue0[0] * n_eU / Variable.stbZgamS[1]
    m_i = m_i + Variable.stbZmue0[0] * m_eU / Variable.stbZgamS[1]
    f_null[1] = Variable.stboMd * n_i - Variable.stboNd * m_i
    for it_dehn in range (0,stbkitmax):
        if (it_dehn <= itmin or it_dehn == 3 or abs(f_null[1]) > stbkepse5):
            # Elongation at break for the next step is determined
            if it_dehn == 3 :
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
                dehn[1] = dehnkrit
            else:
                # Elongation at break for the next step is determined
                Sitdehn(dehn, f_null, it_dehn)
            # Concrete and steel expansions
            Sdehnepscs(dehn[1])

            # Related internal forces of the concrete pressure zone
            n_bU = stbfKnbU()
            m_bU = stbfKmbU()
            n_i = n_bU / Variable.stbZgamC[1]
            m_i = m_bU / Variable.stbZgamC[1]

            # Reduced internal forces of the reinforcement ring
            n_eU = stbfKneU()
            m_eU = stbfKmeU()
            n_i = n_i + Variable.stbZmue0[0] * n_eU / Variable.stbZgamS[1]
            m_i = m_i + Variable.stbZmue0[0] * m_eU / Variable.stbZgamS[1]

            # Function whose zero point is Desired:
            f_null[1] = Variable.stboMd * n_i - Variable.stboNd * m_i

        else:
            break

    if it_dehn == stbkitmax : 
        print('error = ',Variable.stbZbFehler)

    #Fractional cut sizes
    Variable.stbZRNd = n_bU / Variable.stbZgamC[1] + Variable.stbZmue0[0] * n_eU / Variable.stbZgamS[1]
    Variable.stbZRMd = m_bU / Variable.stbZgamC[1] + Variable.stbZmue0[0] * m_eU / Variable.stbZgamS[1]                             #print(Bruch_K)
#------------------------------------------------------------------------------------------------------#

def Snue0_K():
    # Related or reduced internal forces
    dehn = [0,0,0,0]
    f_null = [0,1,0,0]

    # When checking the zero f_null (1) a high accuracy stbkepse7 is required, otherwise
    # The internal balance check does not work for small values ​​of stboNd and stboMd.
    for it_dehn in range(1,stbkitmax+1):
        if it_dehn == 2 or abs(f_null[1]) > stbkepse7: 
            # The strain at break for the next step is determined
            Sitdehn0(dehn, f_null, it_dehn)

            # Concrete and steel strains
            Sdehnepscs(dehn[1])

            # Related internal forces of the concrete pressure zone
            n_bU = stbfKnbU()
            m_bU = stbfKmbU()

            # Function whose zero point is Desired:
            f_null[1] = Variable.stboMd * n_bU - Variable.stboNd * m_bU

        else:
            break

    if it_dehn == stbkitmax :
        print('error = ',Variable.stbZbFehler)

    Variable.stbZnue0 = (abs(n_bU) + m_bU) / (abs(Variable.stboNd) + Variable.stboMd)

    if Variable.stbZnue0 >= Variable.stbogamC[0] - stbkepse5 and Variable.stbZbFehler == False :
        Variable.stbZgamC[1] = Variable.stbogamC[0]
        Variable.stbZgamS[1] = Variable.stbogamS[0]

        # Fractional cut sizes
        Variable.stbZRNd = n_bU / Variable.stbZgamC[1]
        Variable.stbZRMd = m_bU / Variable.stbZgamC[1]

        if Variable.stboii >= 20 :
            # Condition of use
            Gebrauch_K()

    else:
        Variable.stbZnue0 = -Variable.stbZnue0                              #print(Snue0_K)
#------------------------------------------------------------------------------------------------------#

def Gebrauch_K():
    # Condition of use (It is used to determine the Characteristic design related internal forces and values)
    eps1=[0,0,0,0]
    eps2 = [0,0,0,0]
    fnull_m = [0,0,0,0]
    fnull_n = [0,0,0,0]

    Variable.stbZiZ = 2

    # Determination of the uniform basic expansion eps0 for stboMk = 0 #
    if abs(Variable.stboNk) < stbkepse5 :
        eps0 = 0
    elif Variable.stboNk < 0 :

        it_n = 1
        eps2[1] = 0
        Variable.stbZepssk[1] = eps2[1]
        Variable.stbZepsck[1] = eps2[1]
        Variable.stbZepssk[2] = eps2[1]
        Variable.stbZepsck[2] = eps2[1]

        # Related cutting size
        Variable.stbZRNk = stbfalpha() * stbfKnbU() + Variable.stbZmue0[0] * stbfKneU()

        # Function whose zero point is Desired:
        fnull_n[1] = Variable.stboNk - Variable.stbZRNk
        while abs(fnull_n[1]) > stbkepse5 / 2 and it_n < stbkitmax:

            it_n = it_n + 1

            if it_n == 2 :
                fnull_n[2] = fnull_n[1]
                eps2[2] = eps2[1]
                eps2[1] = -Variable.stboepscy
            elif it_n == 3 :
                fnull_n[3] = fnull_n[1]
                eps2[3] = eps2[1]
                eps2[1] = -Variable.stboepscy / 2
            else:
                if fnull_n[1] * fnull_n[2] < 0 :
                    fnull_n[3] = fnull_n[1]
                    eps2[3] = eps2[1]
                else:
                    fnull_n[2] = fnull_n[1]
                    eps2[2] = eps2[1]
                
                eps2[1] = (eps2[2] + eps2[3]) / 2
            
            Variable.stbZepssk[1] = eps2[1]
            Variable.stbZepsck[1] = eps2[1]
            Variable.stbZepssk[2] = eps2[1]
            Variable.stbZepsck[2] = eps2[1]
            # Related cutting size
            Variable.stbZRNk = stbfalpha() * stbfKnbU() + Variable.stbZmue0[0] * stbfKneU()

            # Function whose zero point is Desired:
            fnull_n[1] = Variable.stboNk - Variable.stbZRNk

        if it_n == stbkitmax : 
            Variable.stbZbFehler = True

        eps0 = eps2[1]     

    else:
        Nkgr = math.pi * Variable.stbZmue0[0]   

        if Variable.stboNk <= math.pi * Variable.stbZmue0[0] * Variable.stbofyk / Variable.stboftk :
            eps0 = Variable.stboepssy * Variable.stboNk / (Nkgr * Variable.stbofyk / Variable.stboftk)   

        else:
            eps0 = Variable.stboepssy + (Variable.stboepssu - Variable.stboepssy) * (Variable.stboNk - math.pi * Variable.stbZmue0[0] * Variable.stbofyk / Variable.stboftk) / (Nkgr * (1 - Variable.stbofyk / Variable.stboftk))                     
        

    # The elongation in use must be determined numerically.
    # To do this, the edge strains are varied starting from eps0:
    # eps1 stands for stbZepssk (1)
    # eps2 stands for stbZepsck (1)
    # The moment equilibrium is checked in the outer DO loop (variation of eps1):
    # stboMk - stbfalpha () * m_bU - stbZmue0 (0) * m_eU = 0 #
    # The normal force balance is checked in the inner DO loop (variation of eps2):
    # stboNk - stbfalpha () * n_bU - stbZmue0 (0) * n_eU = 0 #
    it_m = 1
    it_ult = 1
    eps1[1] = eps0
    it_n = 1
    eps2[1] = eps0
    Variable.stbZepssk[1] = eps1[1]
    Variable.stbZepsck[1] = eps2[1]
    Sepsc2s2()
    Variable.stbZRNk = stbfalpha() * stbfKnbU() + Variable.stbZmue0[0] * stbfKneU()
    fnull_n[1] = Variable.stboNk - Variable.stbZRNk

    while abs(fnull_n[1]) > stbkepse5 and it_n < stbkitmax:
        it_n = it_n + 1
        if it_n == 2 :
            fnull_n[2] = fnull_n[1]
            eps2[2] = eps2[1]
            eps2[1] = -Variable.stboepscu
        elif it_n == 3 :
            if fnull_n[1] * fnull_n[2] < 0 :
                fnull_n[3] = fnull_n[1]
                eps2[3] = eps2[1]
                eps2[1] = (eps2[2] + eps2[3]) / 2
            else:
                break
            
        else:
            if fnull_n[1] * fnull_n[2] < 0 :
                fnull_n[3] = fnull_n[1]
                eps2[3] = eps2[1]
            else:
                fnull_n[2] = fnull_n[1]
                eps2[2] = eps2[1]
            
            eps2[1] = (eps2[2] + eps2[3]) / 2
        
        Variable.stbZepssk[1] = eps1[1]
        Variable.stbZepsck[1] = eps2[1]

        Sepsc2s2()

        Variable.stbZRNk = stbfalpha() * stbfKnbU() + Variable.stbZmue0[0] * stbfKneU()
        fnull_n[1] = Variable.stboNk - Variable.stbZRNk

    Variable.stbZRMk = stbfalpha() * stbfKmbU() + Variable.stbZmue0[0] * stbfKmeU()
    fnull_m[1] = Variable.stboMk - Variable.stbZRMk

    # If no solution was found for the balance of normal force in the first iteration step,
    # the first iteration step is repeated with a changed start value.
    while abs(fnull_m[1]) > stbkepse5 and it_ult < stbkitmax:
        it_m = it_m + 1
        it_ult = it_ult + 1
        if it_m == 2 :
            
            # If no solution was found for the balance of normal force in the second iteration step,
            # the second iteration step is repeated with a changed start value.
            if abs(fnull_n[1]) > stbkepse5 :
                it_m = 1
                if fnull_n[1] * Variable.stboNk < 0 :
                    eps1[1] = eps1[1] / 2
                else:
                    eps1[1] = 2 * eps1[1]
                    if Variable.stboNk < 0 :
                        eps1[1] = max(eps1[1], -Variable.stboepscu)
                    else:
                        eps1[1] = min(eps1[1], Variable.stboepssu)
                    
                
            else:
                fnull_m[2] = fnull_m[1]
                eps1[2] = eps1[1]
                eps1[1] = Variable.stboepssu
            
        elif it_m == 3 :
            if abs(fnull_n[1]) > stbkepse5 :
                it_m = 2
                eps1[1] = eps1[1] / 2
            else:
                if fnull_m[1] * fnull_m[2] < 0 :
                    fnull_m[3] = fnull_m[1]
                    eps1[3] = eps1[1]
                else:
                    eps1[3] = Variable.stboepssu
                    eps1[2] = eps1[1]
                
                eps1[1] = (eps1[2] + eps1[3]) / 2
            
        # It is checked whether the solution is included with eps1 (2) and eps1 (1).
        # This is the case if fnull_m (1) * fnull_m (2) <0 # applies.
        # If this is not the case, the solution between eps1 (1) and stboepssu is Desired.
        else:
            if fnull_m[1] * fnull_m[2] < 0 :
                fnull_m[3] = fnull_m[1]
                eps1[3] = eps1[1]
            else:
                fnull_m[2] = fnull_m[1]
                eps1[2] = eps1[1]
            
            eps1[1] = (eps1[2] + eps1[3]) / 2
        
        it_n = 1

        eps2[1] = eps0

        Variable.stbZepssk[1] = eps1[1]
        Variable.stbZepsck[1] = eps2[1]

        Sepsc2s2()

        # Related internal forces
        Variable.stbZRNk = stbfalpha() * stbfKnbU() + Variable.stbZmue0[0] * stbfKneU()
        fnull_n[1] = Variable.stboNk - Variable.stbZRNk

        while abs(fnull_n[1]) > stbkepse5 and it_n < stbkitmax:
            it_n = it_n + 1
            if it_n == 2 :
                fnull_n[2] = fnull_n[1]
                eps2[2] = eps2[1]
                eps2[1] = -Variable.stboepscu
            elif it_n == 3 :
                if fnull_n[1] * fnull_n[2] < 0 :
                    fnull_n[3] = fnull_n[1]
                    eps2[3] = eps2[1]
                    eps2[1] = (eps2[2] + eps2[3]) / 2
                else:
                    break
                
            else:
                if fnull_n[1] * fnull_n[2] < 0 :
                    fnull_n[3] = fnull_n[1]
                    eps2[3] = eps2[1]
                else:
                    fnull_n[2] = fnull_n[1]
                    eps2[2] = eps2[1]
                
                eps2[1] = (eps2[2] + eps2[3]) / 2
            
            Variable.stbZepssk[1] = eps1[1]
            Variable.stbZepsck[1] = eps2[1]

            Sepsc2s2()

            # Related internal forces
            Variable.stbZRNk = stbfalpha() * stbfKnbU() + Variable.stbZmue0[0] * stbfKneU()
            fnull_n[1] = Variable.stboNk - Variable.stbZRNk

        Variable.stbZRMk = stbfalpha() * stbfKmbU() + Variable.stbZmue0[0] * stbfKmeU()
        # Function whose zero point is Desired:
        fnull_m[1] = Variable.stboMk - Variable.stbZRMk

    if it_ult == stbkitmax : 
        Variable.stbZbFehler = True                                                         #print(Gebrauch_K)
#------------------------------------------------------------------------------------------------------#\

def SigVor_K():
    # stbZepssk (1] is fixed via the steel tension stboRissP1
    # The required reinforcement content for maintaining the steel tension stboRissP1 is determined numerically.
    # StbZmue0[0] is used as the starting value, the correct reinforcement content is larger.
    # eps2 stands for stbZepsck [1]
    # Only used when there is min reinforcement required
    faktor=[0,0,0,0]
    eps2 = [0,0,0,0]
    fnull_m = [0,1,0,0]
    fnull_n = [0,1,0,0]  
    Variable.stbZiZ = 2    

    fakmue01_2 = stbfsig_s(Variable.stbZepssk[1]) / Variable.stboRissP1

    # Specification of steel expansion
    if Variable.stboRissP1 <= Variable.stbofyk + 0.1 :
        Variable.stbZepssk[1] = Variable.stboRissP1 / (Variable.stbofyk / Variable.stboepssy)
    else:
        Variable.stbZepssk[1] = Variable.stboepssy + (Variable.stboepssu - Variable.stboepssy) * (Variable.stboRissP1 - Variable.stbofyk) / (Variable.stboftk - Variable.stbofyk)
    
    # Initial value for the iterative determination of the concrete expansion
    # In the middle of a pulling force
    if Variable.stboNk < stbkepse5 :
        eps0 = 0
    else:
        eps0 = Variable.stbZepssk[1]
    
    # There is no concrete compressive force for centric or approximately centric tensile force.
    if Variable.stboNk > stbkepse5 and Variable.stboeNk < stbkepse7 :

        # Central traction
        Variable.stbZepsck[1] = Variable.stbZepssk[1]
        Sepsc2s2()
        faktor[1] = Variable.stboNk / math.pi * Variable.stboftk / Variable.stboRissP1 / Variable.stbZmue0[0]
        Variable.stbZRNk = faktor[1] * Variable.stbZmue0[0] * stbfKneU()
        Variable.stbZRMk = 0
        Variable.stbZmue0[0] = faktor[1] * Variable.stbZmue0[0]

    elif Variable.stboNk > stbkepse5 and Variable.stboeNk < Variable.stboRe / Variable.stboKR :

        # Traction with a small center
        # In the first iteration procedure, the state of expansion is calculated without the participation of the concrete.
        it_m = 1
        eps2[1] = eps0
        Variable.stbZepsck[1] = eps2[1]

        Sepsc2s2()

        fnull_m[1] = Variable.stboeNk - stbfKmeU() / stbfKneU()
        while abs(fnull_m[1]) > stbkepse5 and it_m < stbkitmax:
            it_m = it_m + 1
            if it_m == 2 :
                fnull_m[2] = fnull_m[1]
                eps2[2] = eps2[1]
                eps2[1] = -Variable.stboepscu
            elif it_m == 3 :
                fnull_m[3] = fnull_m[1]
                eps2[3] = eps2[1]
                eps2[1] = (eps2[2] + eps2[3]) / 2
            else:
                if fnull_m[1] * fnull_m[2] < 0 :
                    fnull_m[3] = fnull_m[1]
                    eps2[3] = eps2[1]
                else:
                    fnull_m[2] = fnull_m[1]
                    eps2[2] = eps2[1]               
                eps2[1] = (eps2[2] + eps2[3]) / 2

            Variable.stbZepsck[1] = eps2[1]
            Sepsc2s2()

            fnull_m[1] = Variable.stboeNk - stbfKmeU() / stbfKneU()
        
        #It is checked whether a concrete compressive force occurs or whether no solution was found for the specified steel tension
        if Variable.stbZepsck[1] < 0 or it_m == stbkitmax :
            pass
        #Goes to Moment Iteration

        else:
            it_n = 1
            it_ult = 1
            faktor[1] = 1

            Variable.stbZRNk = faktor[1] * Variable.stbZmue0[0] * stbfKneU()

            fnull_n[1] = Variable.stboNk - Variable.stbZRNk

            while abs(fnull_n[1]) > stbkepse5 and it_ult < stbkitmax:
                it_n = it_n + 1
                it_ult = it_ult + 1          
                if it_n == 2 :
                    fnull_n[2] = fnull_n[1]
                    faktor[2] = faktor[1]
                    faktor[1] = fakmue01_2
                elif it_n == 3 :
                    if fnull_n[1] * fnull_n[2] > 0 :
                        it_n = 2
                        fnull_n[2] = fnull_n[1]
                        faktor[2] = faktor[1]
                        faktor[1] = 2 * faktor[1]
                    else:
                        fnull_n[3] = fnull_n[1]
                        faktor[3] = faktor[1]
                        faktor[1] = (faktor[2] + faktor[3]) / 2
                    
                else:
                    if fnull_n[1] * fnull_n[2] < 0 :
                        fnull_n[3] = fnull_n[1]
                        faktor[3] = faktor[1]
                    else:
                        fnull_n[2] = fnull_n[1]
                        faktor[2] = faktor[1]
                    
                    faktor[1] = (faktor[2] + faktor[3]) / 2
                Variable.stbZRNk = faktor[1] * Variable.stbZmue0[0] * stbfKneU()
                fnull_n[1] = Variable.stboNk - Variable.stbZRNk
            Variable.stbZRMk = faktor[1] * Variable.stbZmue0[0] * stbfKmeU()

    #MomentIteration
    # The normal force balance is checked in the outer DO loop (variation of factor):
    # stboNk - stbfalpha () * n_bU - factor (1) * stbZmue0 (0) * n_eU = 0 #
    # The moment equilibrium is checked in the inner DO loop (variation of eps2):
    # stboMk - stbfalpha () * m_bU - factor (1) * stbZmue0 (0) * m_eU = 0 #
    # In order for this algorithm to converge safely, iterations must be iterated in the inner loop with increased accuracy.
    it_n = 1
    it_ult = 1

    #Initial value for the iterative determination of the reinforcement content
    faktor[1] = 1 
    it_m = 1
    eps2[1] = eps0
    Variable.stbZepsck[1] = eps2[1]

    Sepsc2s2()
    Variable.stbZRMk = stbfalpha() * stbfKmbU() + faktor[1] * Variable.stbZmue0[0] * stbfKmeU()

    fnull_m[1] = Variable.stboMk - Variable.stbZRMk

    while abs(fnull_m[1]) > stbkepse7 and it_m < stbkitmax :
        it_m = it_m + 1
        if it_m == 2 :
            fnull_m[2] = fnull_m[1]
            eps2[2] = eps2[1]
            eps2[1] = -Variable.stboepscu
        elif it_m == 3 :
            fnull_m[3] = fnull_m[1]
            eps2[3] = eps2[1]
            eps2[1] = (eps2[2] + eps2[3]) / 2
        else:
            if fnull_m[1] * fnull_m[2] < 0 :
                fnull_m[3] = fnull_m[1]
                eps2[3] = eps2[1]
            else:
                fnull_m[2] = fnull_m[1]
                eps2[2] = eps2[1]
            eps2[1] = (eps2[2] + eps2[3]) / 2
        Variable.stbZepsck[1] = eps2[1]
        Sepsc2s2()
        Variable.stbZRMk = stbfalpha() * stbfKmbU() + faktor[1] * Variable.stbZmue0[0] * stbfKmeU()
        fnull_m[1] = Variable.stboMk - Variable.stbZRMk

    Variable.stbZRNk = stbfalpha() * stbfKnbU() + faktor[1] * Variable.stbZmue0[0] * stbfKneU()

    fnull_n[1] = Variable.stboNk - Variable.stbZRNk

    while abs(fnull_n[1]) > stbkepse5 and it_ult < stbkitmax:
        it_n = it_n + 1
        it_ult = it_ult + 1             
        if it_n == 2 :
            fnull_n[2] = fnull_n[1]
            faktor[2] = faktor[1]
            faktor[1] = fakmue01_2
        elif it_n == 3 :
            if fnull_n[1] * fnull_n[2] > 0 :
                it_n = 2
                fnull_n[2] = fnull_n[1]
                faktor[2] = faktor[1]
                faktor[1] = 2 * faktor[1]
            else:
                fnull_n[3] = fnull_n[1]
                faktor[3] = faktor[1]
                faktor[1] = (faktor[2] + faktor[3]) / 2
            
        else:
            if fnull_n[1] * fnull_n[2] < 0 :
                fnull_n[3] = fnull_n[1]
                faktor[3] = faktor[1]
            else:
                fnull_n[2] = fnull_n[1]
                faktor[2] = faktor[1]
            
            faktor[1] = (faktor[2] + faktor[3]) / 2
        it_m = 1
        eps2[1] = eps0
        Variable.stbZepsck[1] = eps2[1]

        Sepsc2s2()
        Variable.stbZRMk = stbfalpha() * stbfKmbU() + faktor[1] * Variable.stbZmue0[0] * stbfKmeU()

        fnull_m[1] = Variable.stboMk - Variable.stbZRMk

        while abs(fnull_m[1]) > stbkepse7 and it_m < stbkitmax :
            it_m = it_m + 1
            if it_m == 2 :
                fnull_m[2] = fnull_m[1]
                eps2[2] = eps2[1]
                eps2[1] = -Variable.stboepscu
            elif it_m == 3 :
                fnull_m[3] = fnull_m[1]
                eps2[3] = eps2[1]
                eps2[1] = (eps2[2] + eps2[3]) / 2
            else:
                if fnull_m[1] * fnull_m[2] < 0 :
                    fnull_m[3] = fnull_m[1]
                    eps2[3] = eps2[1]
                else:
                    fnull_m[2] = fnull_m[1]
                    eps2[2] = eps2[1]
                eps2[1] = (eps2[2] + eps2[3]) / 2
            Variable.stbZepsck[1] = eps2[1]
            Sepsc2s2()
            Variable.stbZRMk = stbfalpha() * stbfKmbU() + faktor[1] * Variable.stbZmue0[0] * stbfKmeU()
            fnull_m[1] = Variable.stboMk - Variable.stbZRMk

        Variable.stbZRNk = stbfalpha() * stbfKnbU() + faktor[1] * Variable.stbZmue0[0] * stbfKneU()

        fnull_n[1] = Variable.stboNk - Variable.stbZRNk
        
    if it_ult == stbkitmax :
        Variable.stbZbFehler = True     

    else:
        Variable.stbZmue0[0] = faktor[1] * Variable.stbZmue0[0]                             #print(SigVor_K,faktor[1])
#------------------------------------------------------------------------------------------------------#        

def stbfphix():
    # Simple Mathematical function used in SKnmeU(n_eU1, m_eU1, n_eU2, m_eU2)
    SRechenWerteZ(1)
    R_e1 = 1
    if Variable.stbZeps_s[1] > stbkepse7 :
        if Variable.stbZeps_s[2] < -stbkepse7 :
            xgr = 2 * R_e1 * Variable.stbZeps_s[2] / (Variable.stbZeps_s[2] - Variable.stbZeps_s[1])
            q = (R_e1 - xgr) / R_e1
            if math.sqrt(1 - q ** 2) == 0:
                stbfphix = math.pi / 2 - math.copysign(1,q)*(math.pi / 2)
            else:
                stbfphix = math.pi / 2 - math.atan(q / math.sqrt(1 - q ** 2))
        else:
            stbfphix = 0
    else:
        stbfphix = math.pi
    return stbfphix
#------------------------------------------------------------------------------------------------------#   

def SKnmeU(n_eU1, m_eU1, n_eU2, m_eU2):
    # Limits of integration
    SRechenWerteZ(1)

    # Integration limits for the reinforcement ring
    phiEu = stbfphiEu()
    phiEo = stbfphiEo()
    phix = stbfphix()

    #Elastic Zone
    k1 = (Variable.stbZeps_s[1] + Variable.stbZeps_s[2]) / Variable.stboepssy / 2
    k2 = (Variable.stbZeps_s[1] - Variable.stbZeps_s[2]) / Variable.stboepssy / 2

    #Drawn Zone
    phi_u = phix
    phi_o = phiEo
    n_eU1 = (k1 * phi_o - k2 * math.sin(phi_o))- (k1 * phi_u - k2 * math.sin(phi_u))
    m_eU1 = (k1 * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2))- (k1 * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2))

    #Pressure Zone
    phi_u = phiEu
    phi_o = phix
    n_eU2 = (k1 * phi_o - k2 * math.sin(phi_o))- (k1 * phi_u - k2 * math.sin(phi_u))
    m_eU2 = (k1 * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2))- (k1 * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2))
    
    #Plastic Zone
    k1 = (Variable.stbZeps_s[1] + Variable.stbZeps_s[2]) / (Variable.stboepssu - Variable.stboepssy) / 2
    k2 = (Variable.stbZeps_s[1] - Variable.stbZeps_s[2]) / (Variable.stboepssu - Variable.stboepssy) / 2

    #Drawn Zone
    phi_u = phiEo
    phi_o = math.pi
    n_eU1 = n_eU1 + (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_o - k2 * math.sin(phi_o)) * (Variable.stboftk / Variable.stbofyk - 1) + phi_o) - (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_u - k2 * math.sin(phi_u)) * (Variable.stboftk / Variable.stbofyk - 1) + phi_u)
    m_eU1 = m_eU1 + (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) + math.sin(phi_o)) - (((k1 - Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) + math.sin(phi_u))
    
    #Pressure Zone
    phi_u = 0
    phi_o = phiEu
    n_eU2 = n_eU2 + (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_o - k2 * math.sin(phi_o)) * (Variable.stboftk / Variable.stbofyk - 1) - phi_o)  - (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * phi_u - k2 * math.sin(phi_u)) * (Variable.stboftk / Variable.stbofyk - 1) - phi_u)
    m_eU2 = m_eU2 + (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_o) - k2 / 2 * (phi_o + math.sin(2 * phi_o) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) - math.sin(phi_o))  - (((k1 + Variable.stboepssy / (Variable.stboepssu - Variable.stboepssy)) * math.sin(phi_u) - k2 / 2 * (phi_u + math.sin(2 * phi_u) / 2)) * (Variable.stboftk / Variable.stbofyk - 1) - math.sin(phi_u))
    
    # reduced internal forces
    n_eU1 = n_eU1 * Variable.stbofyk / Variable.stboftk
    m_eU1 = -Variable.stboRe / Variable.stboKR * m_eU1 * Variable.stbofyk / Variable.stboftk
    n_eU2 = n_eU2 * Variable.stbofyk / Variable.stboftk
    m_eU2 = -Variable.stboRe / Variable.stboKR * m_eU2 * Variable.stbofyk / Variable.stboftk

    return n_eU1, m_eU1, n_eU2, m_eU2
#------------------------------------------------------------------------------------------------------#   

def BruchC1S1():
    # The state of fracture (strains), the associated safety factors stbZgamC (1), stbZgamS (1)
    # and the internal forces stbZNucs () and the associated lever arms stbZzi () are determined.
    # For stboNorm = 0 an iterative determination for stbZgamC (1), stbZgamS (1) is required.
    # Related or reduced internal forces
    Nui = [0,0,0]
    Mui = [0,0,0]

    # Determination of the safety factors for the fracture state
    if Variable.stboNorm == 0:
        SgamC1()

    elif Variable.stboNorm > 0:
        if Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2] > Variable.stbZmue0[0] + Variable.stbZmue0[1] + Variable.stbZmue0[2] + stbkepse7:
            Variable.stbZgamC[1] = Variable.stbogamC[1]+(Variable.stbogamC[0] - Variable.stbogamC[1]) * (1 - (Variable.stbZmue0[0] + Variable.stbZmue0[1] + Variable.stbZmue0[2]) / (Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2]))
        else:
            Variable.stbZgamC[1] = Variable.stbogamC[1]
        Variable.stbZgamS[1] = Variable.stbogamS[1]
    
    # Determination of the fracture state (strains)
    Bruch_K()

    # Internal forces and lever arms
    Nui[0] = stbfKnbU()
    Mui[0] = stbfKmbU()
    Variable.stbZNucs[0] = Nui[0] / Variable.stbZgamC[1]
    if Nui[0] < -stbkepse7:
        Variable.stbZzi[0] = Mui[0] / Nui[0] * Variable.stboKR
    else:
        Variable.stbZzi[0] = 0
    
    if Variable.stbZmue0[0] > stbkepse7:
        Nui[1], Mui[1], Nui[2], Mui[2] = SKnmeU(Nui[1], Mui[1], Nui[2], Mui[2])
        if Nui[1] > stbkepse7:
            Variable.stbZNucs[1] = Variable.stbZmue0[0] * Nui[1] / Variable.stbZgamS[1]
            Variable.stbZzi[1] = Mui[1] / Nui[1] * Variable.stboKR
        else:
            Variable.stbZNucs[1] = 0
            Variable.stbZzi[1] = 0
        
        if Nui[2] < -stbkepse7:
            Variable.stbZNucs[2] = Variable.stbZmue0[0] * Nui[2] / Variable.stbZgamS[1]
            Variable.stbZzi[2] = Mui[2] / Nui[2] * Variable.stboKR
        else:
            Variable.stbZNucs[2] = 0
            Variable.stbZzi[2] = 0
        
    else:
        Variable.stbZNucs[1] = 0
        Variable.stbZNucs[2] = 0
        Variable.stbZzi[1] = 0
        Variable.stbZzi[2] = 0

    if Variable.stbZNucs[0] < -stbkepse7 and Variable.stbZNucs[1] > stbkepse7:
        zD = (Variable.stbZzi[0] * Variable.stbZNucs[0] + Variable.stbZzi[2] * Variable.stbZNucs[2]) / (Variable.stbZNucs[0] + Variable.stbZNucs[2])
        Variable.stbZNucs[3] = min(abs(Variable.stbZNucs[0] + Variable.stbZNucs[2]), Variable.stbZNucs[1])
        Variable.stbZzi[3] = Variable.stbZzi[1] - zD
    else:
        Variable.stbZNucs[3] = 0
        Variable.stbZzi[3] = 0                                  #print(BruchC1S1)
#------------------------------------------------------------------------------------------------------#  

def stbfzi():
    # Lever arm of internal forces
    mue1 = 0
    mue2 = 0

    SRechenWerteZ(1)

    mue1 = Variable.stbZmue0[0] / 2
    mue2 = Variable.stbZmue0[0] / 2
    
    # The following modifications for zi are taken from DIN 1045-1: 2008 paragraph 10.3.4 (2).
    # They are necessary to avoid singularities at a small moment.
    stbfzi = Variable.stbZzi[3]

    if Variable.stbZepscd[1] > -stbkepse5 and mue1 > stbkepse7 and mue2 > stbkepse7:
        # fully drawn cross section
        stbfzi = Variable.stboHQ - Variable.stbZ_H[1] - Variable.stbZ_H[2]
    else:
        stbfzi = max(stbfzi, 0.9 * (Variable.stboHQ - Variable.stbZ_H[1]))
        stbfzi = min(stbfzi, max(Variable.stboHQ - 2 * Variable.stbZ_H[2], Variable.stboHQ - Variable.stbZ_H[2] - 0.03))
    return stbfzi
#------------------------------------------------------------------------------------------------------#  

def QuerBemessN0():
    # Shear design for stboNorm = 0
    # The following values ​​are determined:
    # stbZtau0
    # stbZerfas

    # Design value of tensile strength
    f_ctd = stbffctm() / Variable.stbZgamC[1] 

    # Basic value of the shear stress                                                        
    Nd1 = Variable.stboNd * Variable.stboKR ** 2 * Variable.stbofck
    Qd = Variable.stboQd * Variable.stboKR ** 2 * Variable.stbofck
    vormue1 = Variable.stbZmue0[0] / 2 + Variable.stbZmue0[1]
    Rctd = f_ctd * math.pi * Variable.stboKR ** 2
    
    if vormue1 < stbkepse7:
        Variable.stbZtau0 = Qd / stbfAcc()                                      
        sig_x = Nd1 / stbfAcc()                                          
        Variable.stbZtau0 = sig_x / 2 + math.sqrt((sig_x / 2) ** 2 + Variable.stbZtau0 ** 2)   

        if Variable.stbZtau0 <= Variable.stbotau012:
            Variable.stbZerfas = 0

        else:
            Variable.stbZerfas = -1
        
    else:
        if Variable.stbZepscd[2] < stbkepse5:
            # completely suppressed cross section
            Variable.stbZtau0 = Qd / stbfAcc()
            sig_x = Nd1 / stbfAcc()
            Variable.stbZtau0 = sig_x / 2 + math.sqrt((sig_x / 2) ** 2 + Variable.stbZtau0 ** 2)

        else:
            Variable.stbZtau0 = Qd / Variable.stboBQ / stbfzi()
        
        # required shear reinforcement
        if Variable.stbZtau0 <= Variable.stbotau012:
            if Nd1 > Rctd:
                # full thrust coverage
                tau = Variable.stbZtau0

            else:
                # reduced thrust cover
                tau = 0.4 * Variable.stbZtau0
                if Nd1 > 0:
                    tau = tau + (Variable.stbZtau0 - tau) * Nd1 / Rctd
                 
        elif Variable.stbZtau0 <= Variable.stbotau02:
            if Nd1 > Rctd:
                # full thrust coverage
                tau = Variable.stbZtau0

            else:
                # reduced thrust cover
                tau = max(Variable.stbZtau0 ** 2 / Variable.stbotau02, 0.4 * Variable.stbZtau0)
                if Nd1 > 0:
                    tau = tau + (Variable.stbZtau0 - tau) * Nd1 / Rctd
                
            
        elif Variable.stbZtau0 <= Variable.stbotau03:
            if Variable.stbZepscd[1] > -stbkepse5:
                #impermissibly high shear load
                tau = -1 

            else:
                # full thrust coverage
                tau = Variable.stbZtau0
            
        else:
            #impermissibly high shear load
            tau = -1
        
        if tau <= -0.5:
            Variable.stbZerfas = -1
        else:
            Variable.stbZerfas = tau * Variable.stboBQ / (Variable.stbofyk / Variable.stbogamS[1]) * 10000                      #print(QuerBemessN0)
#------------------------------------------------------------------------------------------------------#  

def QuerBemessN123():
    # Shear design for stboNorm> 0
    # The following values ​​are determined for unreinforced cross sections:
    # stbZerfas
    # stbZminas
    # stbZVRdc
    # stbZtaucp
    # stbZfcvd
    # The following values ​​are determined for reinforced cross-sections:
    # stbZerfas
    # stbZminas
    # stbZVRdc
    # stbZVRdmax
    # stbZcottheta
    # [1] = DIN 1045: 2008
    # [2] = EN 1992-1-1: 2004 (Eurocode 2)
    # [3] = DIN EN 1992-1-1: 2004 + AC: 2010 + NA: 2011, cited here from the EUROCODE 2 standards manual for Germany, commented version, 1st edition 2012
    # The variable names are largely based on the formula symbols in [3]
    zi = 0

    SRechenWerteZ(1)

    # Design value of compressive strength
    f_cd = Variable.stbofck / Variable.stbZgamC[1]   

    #Design value of tensile strength                                                             
    f_ctd = stbffctm() / Variable.stbZgamC[1]  

    # Design value of compressive Reinforcement yield strength                                                         
    f_yd = Variable.stbofyk / Variable.stbogamS[1]   

    Nd1 = Variable.stboNd * Variable.stboKR ** 2 * Variable.stbofck
    Qd = Variable.stboQd * Variable.stboKR ** 2 * Variable.stbofck
    vormue1 = Variable.stbZmue0[0] / 2 + Variable.stbZmue0[1]
    Rctd = f_ctd * math.pi * Variable.stboKR ** 2

    if vormue1 < stbkepse7:
        # medium compressive stress: sigcp is positive for compressive stresses and negative for tension
        if Variable.stboNorm == 1:
            sigcp = -Nd1 / Variable.stboBQ / Variable.stboHQ     # [1]                                                 
        elif Variable.stboNorm == 2 or Variable.stboNorm == 3:   # [2],[3]
            sigcp = -Nd1 / stbfAcc()                                                             

        # Determine stbZtaucp, stbZfcvd, stbZVRdc                                                                       
        if Variable.stboNorm == 1:
            Variable.stbZtaucp = 1.5 * Qd / Variable.stboBQ / Variable.stboHQ      #[1]                                       
            Variable.stbZfcvd = math.sqrt(f_ctd ** 2 + sigcp * f_ctd)   

        elif Variable.stboNorm == 2 or Variable.stboNorm == 3:
            Variable.stbZtaucp = 1.5 * Qd / stbfAcc()                                                   
            sig_clim = f_cd - 2 * math.sqrt(f_ctd * (f_ctd + f_cd))                #[2], [3]              
            if sigcp <= sig_clim:                                                         
                Variable.stbZfcvd = math.sqrt(f_ctd ** 2 + sigcp * f_ctd)
            else:
                Variable.stbZfcvd = math.sqrt(max(f_ctd ** 2 + sigcp * f_ctd - (sigcp - sig_clim) ** 2 / 4, 0))
            
            Variable.stbZVRdc = stbfAcc() * Variable.stbZfcvd / 1.5

        # Minimum shear reinforcement [cm ^ 2 / m]
        Variable.stbZminas = 0

        # required shear reinforcement
        if Qd <= Variable.stbZVRdc + stbkepse5:
            Variable.stbZerfas = 0
        else:
            Variable.stbZerfas = -1

    else:
        # Lever arm of internal forces
        zi = stbfzi()

        # static usable height [1],[2] and [3]
        DQ = Variable.stboHQ - Variable.stbZ_H[1]    

        #Average compressive stress in relation to the total cross-section: sigcp is positive for compressive stresses and negative for tension
        # [1]                                      
        sigcp = -Nd1 / Variable.stboBQ / Variable.stboHQ   

        # Determine stbZVRdc [1]                                        
        vorAs1 = 10000 * vormue1 * Variable.stboBQ * Variable.stboHQ * Variable.stbofck / Variable.stboftk
        rho1 = min(vorAs1 / 10000 / Variable.stboBQ / DQ, 0.02)
        kappa = min(1 + math.sqrt(0.2 / DQ), 2)

        if Variable.stboNorm == 1 or Variable.stboNorm == 3:
            k1 = 0.12
            k2 = 0.15
            if DQ <= 0.6:
                kappa1 = 0.0525
            elif DQ > 0.8:
                kappa1 = 0.0375
            else:
                kappa1 = 0.0525 - 0.015 * (DQ - 0.6) / 0.2
            
            nuemin = kappa1 / (stbfalpha() * Variable.stbZgamC[1]) * math.sqrt(kappa ** 3 * Variable.stbofck)
        elif Variable.stboNorm == 2:
            k1 = 0.15
            k2 = 0.18
            kappa1 = 0.035
            nuemin = kappa1 * math.sqrt(kappa ** 3 * Variable.stbofck)
        
        if Variable.stboNorm == 1:
            Variable.stbZVRdc = (k2 / (stbfalpha() * Variable.stbZgamC[1]) * kappa * (100 * rho1 * Variable.stbofck) ** (1 / 3) + k1 * sigcp) * Variable.stboBQ * DQ  
            VRdctmin = (nuemin + k1 * sigcp) * Variable.stboBQ * DQ
        elif Variable.stboNorm == 2 or Variable.stboNorm == 3:
            Variable.stbZVRdc = (k2 / (stbfalpha() * Variable.stbZgamC[1]) * kappa * (100 * rho1 * Variable.stbofck) ** (1 / 3) + k1 * min(sigcp, 0.2 * f_cd)) * Variable.stboBQ * DQ  
            VRdctmin = (nuemin + k1 * min(sigcp, 0.2 * f_cd)) * Variable.stboBQ * DQ                                                                       
        
        Variable.stbZVRdc = max(max(Variable.stbZVRdc, VRdctmin), 0)

        # Determine stbZcottheta and stbZVRdmax
        if Variable.stboNorm == 1 or Variable.stboNorm == 3:
            nue1 = 0.75                              #[1]  and [3]                                        
        elif Variable.stboNorm == 2:
            nue1 = 0.6                               #[2]                                  
        
        if Qd <= Variable.stbZVRdc + stbkepse5:
            Variable.stbZcottheta = 1
            Variable.stbZVRdmax = Variable.stboBQ * zi * nue1 * f_cd / (Variable.stbZcottheta + 1 / Variable.stbZcottheta)
        else:
            if Variable.stboNorm == 1 or Variable.stboNorm == 3:
                if Nd1 > Rctd:
                    maxcot = 1                                                                
                else:
                    VRdc = 0.24 * Variable.stbofck ** (1 / 3) * (1 - 1.2 * sigcp / f_cd) * Variable.stboBQ * zi 
                    if 1 - VRdc / Qd < stbkepse7:                                        
                        maxcot = 3                                                         
                    else:
                        maxcot = min((1.2 + 1.4 * sigcp / f_cd) / (1 - VRdc / Qd), 3)
                    if Nd1 > 0:
                        maxcot = 1 + (maxcot - 1) * (Rctd - Nd1) / Rctd                        
            elif Variable.stboNorm == 2:
                maxcot = 2.5
            if Variable.stbomaxcottheta > stbkepse3:
                maxcot = min(max(Variable.stbomaxcottheta, 1), maxcot)                 
            Variable.stbZVRdmax = Variable.stboBQ * zi * nue1 * f_cd / (maxcot + 1 / maxcot)                     
            if Qd <= Variable.stbZVRdmax + stbkepse5:
                Variable.stbZcottheta = maxcot
            elif Qd <= Variable.stboBQ * zi * nue1 * f_cd / (1 + 1 / 1) + stbkepse5:           
                Term = 2 * Qd / (Variable.stboBQ * zi * nue1 * f_cd)
                theta = 0.5 *  math.atan(Term / math.sqrt(-Term * Term + 1))
                Variable.stbZcottheta = max(1 / math.tan(theta), 1)
                Variable.stbZVRdmax = Variable.stboBQ * zi * nue1 * f_cd / (Variable.stbZcottheta + 1 / Variable.stbZcottheta)
            else:                                                                              
                Variable.stbZcottheta = 1
                Variable.stbZVRdmax = Variable.stboBQ * zi * nue1 * f_cd / (Variable.stbZcottheta + 1 / Variable.stbZcottheta)
        
        # Minimum shear reinforcement [cm ^ 2 / m]
        if Variable.stboNorm == 1 or Variable.stboNorm == 3:                                                  
            Variable.stbZminas = 0.16 * stbffctm() / Variable.stbofyk * Variable.stboBQ * 10000                           
        elif Variable.stboNorm == 2:
            Variable.stbZminas = 0.08 * math.sqrt(Variable.stbofck) / Variable.stbofyk * Variable.stboBQ * 10000                        
        
        # required shear reinforcement
        if Qd <= Variable.stbZVRdc + stbkepse5:
            Variable.stbZerfas = Variable.stbZminas
        elif Qd <= Variable.stbZVRdmax + stbkepse5:
            Variable.stbZerfas = Qd / f_yd / zi / Variable.stbZcottheta * 10000
            if Variable.stbZerfas < Variable.stbZminas:
                Variable.stbZerfas = Variable.stbZminas
                if Variable.stbZcottheta > 1 + stbkepse5 and Variable.stbomaxcottheta <= stbkepse3:

                    # stbZcottheta is reduced so that stbZerfas = stbZminas applies
                    Variable.stbZcottheta = max(Qd / f_yd / zi / Variable.stbZerfas * 10000, 1)   

                    #for the reduced value of stbZcottheta there is a higher value of stbZVRdmax        
                    Variable.stbZVRdmax = Variable.stboBQ * zi * nue1 * f_cd / (Variable.stbZcottheta + 1 / Variable.stbZcottheta) 
        
        else:
            Variable.stbZerfas = -1                                 #print( QuerBemessN123)
#------------------------------------------------------------------------------------------------------#  

def stbfAcc():
    xgr = 0
    q = 0
    phi0 = 0
    if Variable.stbZepscd[2] < stbkepse7:
        stbfAcc = math.pi * Variable.stboKR ** 2
        
    elif Variable.stbZepscd[1] > -stbkepse7:
        stbfAcc = 0

    else:
        xgr = Variable.stboD * Variable.stbZepscd[1] / (Variable.stbZepscd[1] - Variable.stbZepscd[2])
        q = (Variable.stboKR - xgr) / Variable.stboKR
        phi0 = math.pi / 2 -  math.atan(q / math.sqrt(1 - q ** 2))
        stbfAcc = Variable.stboKR ** 2 * (2 * phi0 - math.sin(2 * phi0)) / 2

    return stbfAcc
#------------------------------------------------------------------------------------------------------#  

#------------------------------------------------------------------------------------------------------#  
#################################----End of Module----################################################
#------------------------------------------------------------------------------------------------------#  

if __name__ == "__main__":
    for i in range(11,29):
        print(StB_K_MN(2, 1.5, 1.15,810,0, 600,0 ,700, 98, 0 ,45, 0.909090909, 0.002, 0.0035, 2, 0.1818182, "0.10 0.2" ,500, 525, 200000, 0.025, 240,1,i))
    for i in range(11,24):
        print(StB_K_Q(2, 1.5, 1.15, 810, 0, 1607 ,700, 98, 0 ,45, 0.9090909, 0.002, 0.0035, 2.00, 0.181818182, "0.10 0.2",500, 525, 200000, 0.025, 0,0,0,i))
#     # A = StB_K_MN(2, 1.5, 1.15, 1.35*90.03, 1.35*-624.9, 90.03, -624.9, 900, 100, 0.0, 35.0, 0.91, 0.002, 0.0035, 2.0, 0.18, '0.1 0.2', 500, 525, 200000.0, 0.025, 0,1, 17)
#     # print(StB_K_MN(2, 1.5, 1.15, 1.35*90.03, 1.35*-624.9, 90.03, -624.9, 900, 100, 0.0, 35.0, 0.91, 0.002, 0.0035, 2.0, 0.18, '0.1 0.2', 500, 525, 200000.0, 0.025, 0,1, 17))
#     # print(StB_K_Q(2, 1.5, 1.15, 1.35*90.03, 1.35*-624.9, 1.35*-634.4, 900, 100, A, 35.0, 0.91, 0.002, 0.0035, 2.0, 0.18, '0.1 0.2', 500, 525, 200000.0, 0.025, 0.0, 0.0, 0.0, 19))

#------------------------------------------------------------------------------------------------------#  
#################################----End of Codee----################################################
#------------------------------------------------------------------------------------------------------# 