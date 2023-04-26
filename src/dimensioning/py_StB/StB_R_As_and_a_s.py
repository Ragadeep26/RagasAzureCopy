###----DIMENSIONING OF CIRCULAR REINFORCEMNT-----###
'''
Date of Original Version -26th July, 2017 -
Date of Python version - 18th Feb, 2020 - ----
'''
###----Python Version created by RAGADEEP BOJJA (Translate of 0_stb created in VBA by Dr. Berthold Klobe)----###
#------------------------------------------------------------------------------------------------------#
#
#Required Modules
import math 
#import Klobe3_GlobalVarR as Variable
from src.dimensioning.py_StB import GlobalVarR as Variable

stbkitmax = 50
stbkepse3 = 0.0001
stbkepse5 =0.00001
stbkepse7 = 0.0000001
#stbofck (beta_WN) = 15
stbk15tau012 = 0.5
stbk15tau02 = 1.2
stbk15tau03 = 2
stbk15tau1 = 1.4     
stbk15tau2 = 0.7     
#stbofck (beta_WN) = 25
stbk25tau012 = 0.75
stbk25tau02 = 1.8
stbk25tau03 = 3
stbk25tau1 = 1.8     
stbk25tau2 = 0.9     
#stbofck (beta_WN) = 35
stbk35tau012 = 1
stbk35tau02 = 2.4
stbk35tau03 = 4
stbk35tau1 = 2.2     
stbk35tau2 = 1.1     
#stbofck (beta_WN) = 45
stbk45tau012 = 1.1
stbk45tau02 = 2.7
stbk45tau03 = 4.5
stbk45tau1 = 2.6     
stbk45tau2 = 1.3     
#stbofck (beta_WN) = 55
stbk55tau012 = 1.25
stbk55tau02 = 3
stbk55tau03 = 5
stbk55tau1 = 3      
stbk55tau2 = 1.5  
stbkKemax = 0.3803
stbkRemax = 0.4

def RechenWerte(Norm, gam_c, gam_s, Md, Nd, Qd, Mk, Nk,DD, BB, HH_, H__, sym0 , vorAs0, delta, vorAs1, vorAs2, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K,f_yk, f_tk, Es, eps_su, RissP1, minBew, TauP1, TauP2, TauP3, ii):
    Variable.stboNorm = Norm
    Variable.stboQuer = 3
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
    
    Variable.stbofck = f_ck
    Variable.stboalpha = alpha
    Variable.stboepscy = eps_cy
    Variable.stboepscu = eps_cu
    Variable.stbon2 = n2

    Variable.stbofyk = f_yk
    Variable.stboftk = f_tk
    Variable.stboepssy = f_yk / Es
    Variable.stboepssu = eps_su
    Variable.Nd1 = 0
    if Variable.stboQuer == 1 or Variable.stboQuer == 2:
        Variable.stboNd = Nd / 1000 / Variable.stboKR ** 2 / Variable.stbofck
        Variable.stboMd = abs(Md) / 1000 / Variable.stboKR ** 3 / Variable.stbofck
        Variable.stboQd = abs(Qd) / 1000 / Variable.stboKR ** 2 / Variable.stbofck
        Variable.stboNk = Nk / 1000 / Variable.stboKR ** 2 / Variable.stbofck
        Variable.stboMk = abs(Mk) / 1000 / Variable.stboKR ** 3 / Variable.stbofck
        Variable.stboHQ = Variable.stboD * math.sqrt(math.pi / 4)
        Variable.stboBQ = Variable.stboD * math.sqrt(math.pi / 4)
    elif Variable.stboQuer == 3:
        Variable.stboNd = Nd/ 1000 / Variable.stboRB / Variable.stboD / Variable.stbofck
        Variable.stboMd = abs(Md) / 1000 / Variable.stboRB / Variable.stboD ** 2 / Variable.stbofck
        Variable.stboQd = abs(Qd) / 1000 / Variable.stboRB / Variable.stboD / Variable.stbofck
        Variable.stboNk = Nk / 1000 / Variable.stboRB / Variable.stboD / Variable.stbofck
        Variable.stboMk = abs(Mk) / 1000 / Variable.stboRB / Variable.stboD ** 2 / Variable.stbofck
        Variable.stboHQ = Variable.stboD
        Variable.stboBQ = Variable.stboRB

    if abs(Variable.stboNd) < stbkepse7:
        Variable.stboeNd = Variable.stboMd / stbkepse7
    else:
        Variable.stboeNd = Variable.stboMd / Variable.stboNd
    
    if abs(Variable.stboNk) < stbkepse7:
        Variable.stboeNk = Variable.stboMk / stbkepse7
    else:
        Variable.stboeNk = Variable.stboMk / Variable.stboNk

    if abs(Variable.stboNd) < stbkepse5 and Variable.stboMd < stbkepse5:
        Variable.stboNullSd = True
        Variable.stboVMd = 0
        Variable.stboNullSk = True
        Variable.stboVMk = 0
    else:
        Variable.stboNullSd = False
        if Md >= 0:
            Variable.stboVMd = 0
        else:
            Variable.stboVMd = 1
        
        if abs(Variable.stboNk) < stbkepse5 and Variable.stboMk < stbkepse5:
            Variable.stboNullSk = True
        else:
            Variable.stboNullSk = False
            if Mk >= 0:
                Variable.stboVMk = 0
            else:
                Variable.stboVMk = 1


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
    
    SgamCSini(gam_c, gam_s, delt_S, delt_K)

    Variable.stbZiZ = 1                  

    if (abs(Variable.stboeNd - stbfeBew()) < stbkepse7 and Variable.stboNd > stbkepse5) or (abs(Variable.stboeNd) < stbkepse7 and Variable.stboNd < -stbkepse5) or((Variable.stboVMd != Variable.stboVMk or sym0 == True) and Variable.stbobHkrit == False):
        Variable.stbosymmue0 = True
    else:
        Variable.stbosymmue0 = False

    Variable.stboRissP1 = RissP1
    Variable.stbZiZ = 1            
    Sdehnkrit()

    if Variable.stboNachweis == 1:
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
        Variable.stbZiZ = 1
        Variable.stbZmue0[0] = Variable.stbovormue0[0]
        Variable.stbZmue0[1] = Variable.stbovormue0[1]
        Variable.stbZmue0[2] = Variable.stbovormue0[2]
        Variable.stbZgamC[1] = Variable.stbogamC[1]
        Variable.stbZgamS[1] = Variable.stbogamS[1]

        
        for i in range(0,4):
            Variable.stbZNucs[i] = 0
            Variable.stbZzi[i] = 0

        if Variable.stboNorm == 0:
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
    if Variable.stboNorm < 0 or Variable.stboD < stbkepse5 or ((Variable.stboQuer == 1 or Variable.stboQuer == 2) and Variable.stboKR < stbkepse5) or (Variable.stboQuer == 3 and Variable.stboRB < stbkepse5) or Variable.stboD - Variable.stboH[1] - Variable.stboH[2] < -stbkepse5 or Variable.stbofck < stbkepse5 or Variable.stboalpha < stbkepse5 or Variable.stboepscy < stbkepse7 or Variable.stboepscu < Variable.stboepscy - stbkepse7 or Variable.stbofyk < stbkepse5 or Variable.stboftk < Variable.stbofyk - stbkepse5 or Variable.stboepssy < stbkepse7 or Variable.stboepssu < Variable.stboepssy - stbkepse7 or Variable.stbogamC[0] < stbkepse5 or Variable.stbogamC[1] < stbkepse5 or Variable.stbogamS[0] < stbkepse5 or Variable.stbogamS[1] < stbkepse5 or (Variable.stboNachweis == 2 and Variable.stbotau02 < Variable.stbotau012 - stbkepse7) or (Variable.stboNachweis == 2 and Variable.stbotau03 < Variable.stbotau02 - stbkepse7):
        Variable.stbZbFehler = True
    else:
        Variable.stbZbFehler = False
    #print(RechenWerte)


def SRechenWerteZ(InOut):
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
            Variable.stbZepssk[2] = Variable.stbZeps_s[2]
    #print (SRechenWerteZ)

def SgamCSini(gam_c, gam_s, delt_S, delt_K):
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
    Smue0Druc(delt_S, delt_K)
    #print(SgamCSini)

def stbfeBew():
    SRechenWerteZ(1)
    if Variable.stboQuer == 3 and Variable.stbobHkrit == True:
        stbfeBew = (Variable.stbZ_H[2] - Variable.stbZ_H[1]) / 2 / Variable.stboD
    else:
        stbfeBew = 0
    return stbfeBew


def Sdehnkrit():
    n_eU = [0,0,0]
    m_eU = [0,0,0]
    dehn = [0,0,0,0]  
    f_null = [0,1,0,0]  
    SRechenWerteZ(1)
    if Variable.stboQuer == 3 :
        for it_dehn in range (1,stbkitmax):
            if abs(f_null[1]) > stbkepse5:
                Sitdehn(dehn, f_null, it_dehn)
                Sdehnepscs(dehn[1])
                n_eU[1] = stbfRneU1()
                m_eU[1] = stbfRmeU1()
                n_eU[2] = stbfRneU2()
                m_eU[2] = stbfRmeU2()
                f_null[1] = n_eU[1] + n_eU[2] + m_eU[1] + m_eU[2]
            else:
                break
    Variable.stbodehnkrit[1] = dehn[1]
    if Variable.stboQuer == 3 :
        for it_dehn in range (1,stbkitmax):
            if abs(f_null[1]) > stbkepse5:
                Sitdehn(dehn, f_null, it_dehn)
                Sdehnepscs(dehn[1])
                n_eU[1] = stbfRneU1()
                m_eU[1] = stbfRmeU1()
                f_null[1] = n_eU[1] + m_eU[1]
            else:
                break
    Variable.stbodehnkrit[2] = dehn[1]
    Variable.stbZepscd[2] = Variable.stboepssu + (Variable.stboepssu + Variable.stboepscu) * Variable.stbZ_H[1] / (Variable.stboD - Variable.stbZ_H[1])   
    Variable.stbodehnkrit[3] = -0.5 * (Variable.stbZepscd[2] - Variable.stboepscu) / Variable.stbZepscd[2]           
    dehn[1] = -1
    dehn[2] = Variable.stbodehnkrit[3]
    dehn[3] = 1
    Variable.stbZgamC[1] = Variable.stbogamC[0]
    Variable.stbZgamS[1] = Variable.stbogamS[0]
    Variable.stbZgamC[2] = Variable.stbogamC[1]
    Variable.stbZgamS[2] = Variable.stbogamS[1]
    Variable.stbZgamC[3] = Variable.stbogamC[1]
    Variable.stbZgamS[3] = Variable.stbogamS[1]
    if Variable.stboQuer == 3 :
        for k in range(1,4):
            Sdehnepscs(dehn[k])
            n_bU = stbfRnbU()
            m_bU = stbfRmbU()
            n_eU[1] = stbfRneU1()
            m_eU[1] = stbfRmeU1()
            n_eU[2] = stbfRneU2()
            m_eU[2] = stbfRmeU2()
            Variable.stbomue0Dehn[1][k] = ((Variable.stboNd - n_bU / Variable.stbZgamC[k]) * m_eU[2] / Variable.stbZgamS[k] - (Variable.stboMd - m_bU / Variable.stbZgamC[k]) * n_eU[2] / Variable.stbZgamS[k]) / (n_eU[1] / Variable.stbZgamS[k] * m_eU[2] / Variable.stbZgamS[k] - m_eU[1] / Variable.stbZgamS[k] * n_eU[2] / Variable.stbZgamS[k])
            Variable.stbomue0Dehn[2][k] = (n_eU[1] / Variable.stbZgamS[k] * (Variable.stboMd - m_bU / Variable.stbZgamC[k]) - m_eU[1] / Variable.stbZgamS[k] * (Variable.stboNd - n_bU / Variable.stbZgamC[k])) / (n_eU[1] / Variable.stbZgamS[k] * m_eU[2] / Variable.stbZgamS[k] - m_eU[1] / Variable.stbZgamS[k] * n_eU[2] / Variable.stbZgamS[k])
            if Variable.stbomue0Dehn[1][k] < 0 or Variable.stbomue0Dehn[2][k] < 0 :
                Variable.stbomue0Dehn[3][k] = -1
            else:
                Variable.stbomue0Dehn[3][k] = Variable.stbomue0Dehn[1][k] + Variable.stbomue0Dehn[2][k]


def Smue0Riss():
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
    Variable.stbZiZ = 1
    if Variable.stboNorm == 0:
        Variable.stbZgamC[1] = 1 / Variable.stboalpha
    elif Variable.stboNorm > 0:
        Variable.stbZgamC[1] = Variable.stbogamC[1]
    Variable.stbZgamS[1] = 1
    if Variable.stboNorm == 0:
        Variable.stbofyk = 0.8 * Variable.stbofyk
        Variable.stboftk = Variable.stbofyk
    elif Variable.stboNorm > 0:
        Variable.stbofyk = Variable.stbofyk
        Variable.stboftk = Variable.stbofyk
    
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
    Variable.stboMd =  stbffctm() / Variable.stbofck / 6
    Serfmue0_R()
    Variable.stbZerfmue0[0] = 0 
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
    Variable.stbomue0Druc[2] = EingangWerte[9]
    #print(Smue0Riss)


def Smue0Druc(delt_S, delt_K):
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
                # else:
                #     mue0min = max((StrVek[2]) / 100, 0) * Variable.stboftk / Variable.stbofck
                
                if Variable.stboQuer == 3:
                    Variable.stbomue0Druc[0] = 0
                    Variable.stbomue0Druc[1] = max(NEdmin * abs(Variable.stboNd) * Variable.stbogamS[1] / 2 * Variable.stboftk / Variable.stbofyk, mue0min) / 2
                    Variable.stbomue0Druc[2] = Variable.stbomue0Druc[1] 
            else:
                NEdmin = StrVek[0]
                if Variable.stboQuer == 3:
                    Variable.stbomue0Druc[0] = 0
                    Variable.stbomue0Druc[1] = NEdmin * abs(Variable.stboNd) * Variable.stbogamS[1] * Variable.stboftk / Variable.stbofyk / 2
                    Variable.stbomue0Druc[2] = Variable.stbomue0Druc[1]  
        else:     
            Variable.stbomue0Druc[0] = 0
            Variable.stbomue0Druc[1] = 0
            Variable.stbomue0Druc[2] = 0
    #print(Smue0Druc)


def stbffctm():
    if Variable.stboNorm == 0:
        stbffctm = 0.25 * max(Variable.stbofck, 35) ** (2 / 3)
    elif Variable.stboNorm > 0:
        if Variable.stbofck < 52.5:
            stbffctm = 0.3 * Variable.stbofck ** (2 / 3)
        else:
            stbffctm = 2.12 * math.log(1 + (Variable.stbofck + 8) / 10)
    #print(stbffctm)
    return stbffctm


def Sdehnepscs(dehn):
    SRechenWerteZ(1)
    #Variable.imag = Variable.imag+1
    #arrdehn.append(Variable.imag)
    if dehn < -0.5:
        Variable.stbZeps_c[1] = -Variable.stboepscu + (Variable.stboepscu - Variable.stboepscy) * (-0.5 - dehn) / 0.5
    elif dehn < 0:
        Variable.stbZeps_c[1] = -Variable.stboepscu
    else:
        Variable.stbZeps_c[1] = -Variable.stboepscu + dehn * (Variable.stboepscu + Variable.stboepssu)
    if dehn < -0.5:
        eps_gr = -Variable.stboepscu * Variable.stbZ_H[1] / Variable.stboD
        Variable.stbZeps_s[1] = eps_gr + (Variable.stboepscy + eps_gr) * (dehn + 0.5) / 0.5
    elif dehn < 0:
        eps_gr = -Variable.stboepscu * Variable.stbZ_H[1] / Variable.stboD
        Variable.stbZeps_s[1] = Variable.stboepssu + (Variable.stboepssu - eps_gr) * dehn / 0.5
    else:
        Variable.stbZeps_s[1] = Variable.stboepssu
    SRechenWerteZ(2)
    Sepsc2s2()
    #print(Sdehnepscs)
    #print(1)
def Sepsc2s2():
    SRechenWerteZ(1)
    Variable.stbZeps_c[2] = Variable.stbZeps_c[1] + (Variable.stbZeps_s[1] - Variable.stbZeps_c[1]) * Variable.stboD / (Variable.stboD - Variable.stbZ_H[1])
    Variable.stbZeps_s[2] = Variable.stbZeps_c[1] + (Variable.stbZeps_s[1] - Variable.stbZeps_c[1]) * Variable.stbZ_H[2] / (Variable.stboD - Variable.stbZ_H[1])
    SRechenWerteZ(2)
    #print(Sepsc2s2)
    #print(2)

def Sitdehn(dehn, f_null, it_dehn):
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
        if Variable.Nd1 < -stbkepse5:
            if f_null[1] * f_null[2] < 0:
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
            else:
                dehn[2] = dehn[1]
                f_null[2] = f_null[1]
            
        else:
            if f_null[1] * f_null[3] < 0:
                dehn[2] = dehn[1]
                f_null[2] = f_null[1]
            else:
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
        dehn[1] = (dehn[2] + dehn[3]) / 2
    #print(Sitdehn)

def stbfsig_s(eps_s):
    if abs(eps_s) <= Variable.stboepssy:
        stbfsig_s = eps_s / Variable.stboepssy * Variable.stbofyk
    elif abs(eps_s) <= Variable.stboepssu:
        stbfsig_s = math.copysign(1,eps_s) * (Variable.stbofyk + (Variable.stboftk - Variable.stbofyk) * (abs(eps_s) - Variable.stboepssy) / (Variable.stboepssu - Variable.stboepssy))
    else:
        stbfsig_s = math.copysign(1,eps_s) * Variable.stboftk
    return stbfsig_s

def stbfalpha():
    if Variable.stboNorm == 0 or Variable.stboNorm == 1:
        stbfalpha = Variable.stboalpha
    elif Variable.stboNorm == 2 or Variable.stboNorm == 3:
        stbfalpha = Variable.stboalpha * Variable.stbogamC[1] / Variable.stbZgamC[1]
    return stbfalpha

def Sitdehn0(dehn, f_null, it_dehn):
    if it_dehn == 1:
        f_null[1] = 0
        dehn[1] = -1
    elif it_dehn == 2:
        dehn[2] = dehn[1]
        f_null[2] = f_null[1]
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
        
        dehn[1] = (dehn[2] + dehn[3]) / 2
    #print(Sitdehn0)



def Smue0opt(it_mue, mue_loop):
    bEnd = False
    if Variable.stbZerfmue0[1] < 0 or Variable.stbZerfmue0[2] < 0:
        sum_mue0 = -1
    else:
        sum_mue0 = Variable.stbZerfmue0[1] + Variable.stbZerfmue0[2]
    
    Variable.mimue0[1][2] = sum_mue0

    if it_mue == 1:
        if Variable.stbosymmue0==True or Variable.stbZerfmue0[2] <= Variable.stbovormue0[2] + stbkepse5:
            Variable.mue_loop = False
        else:
            Variable.mimue0[0][4] = Variable.stbZerfmue0[2]
            Variable.mimue0[1][4] = sum_mue0
            Variable.stbZerfmue0[2] = Variable.stbovormue0[2]
            Variable.stbZsymm = False
            Variable.mue_loop = True
        
    elif it_mue == 2:
        Variable.mimue0[0][0] = Variable.stbZerfmue0[2]
        Variable.mimue0[1][0] = sum_mue0
        Variable.mimue0[0][2] = Variable.mimue0[0][4]
        Variable.mimue0[1][2] = Variable.mimue0[1][4]
        if (Variable.mimue0[1][0] < Variable.mimue0[1][2] and Variable.mimue0[1][0] >= 0) or Variable.mimue0[1][2] < 0:
            Variable.mimue0[0][2] = Variable.mimue0[0][0]
            Variable.mimue0[1][2] = Variable.mimue0[1][0]
        
        for k in range(1,4):
            if (Variable.stbomue0Dehn[3][k] < Variable.mimue0[1][2] and Variable.stbomue0Dehn[3][k] >= 0) or Variable.mimue0[1][2] < 0:
                Variable.mimue0[0][2] = Variable.stbomue0Dehn[2][k]
                Variable.mimue0[1][2] = Variable.stbomue0Dehn[3][k]

        Variable.stbZerfmue0[2] = Variable.mimue0[0][2]
    elif it_mue == 3:
        Variable.stbZerfmue0[2] = max(Variable.mimue0[0][2] - stbkepse3, Variable.stbovormue0[2])
    elif it_mue == 4:
        Variable.mimue0[0][1]= Variable.stbZerfmue0[2]
        Variable.mimue0[1][1] = sum_mue0
        Variable.stbZerfmue0[2] = max(Variable.mimue0[0][2] + stbkepse3, Variable.stbovormue0[2])
    elif it_mue == 5:
        Variable.mimue0[0][3] = Variable.stbZerfmue0[2]
        Variable.mimue0[1][3] = sum_mue0
        bEnd = False
        if Variable.mimue0[1][2] < 0 or Variable.mimue0[1][2] > Variable.mimue0[1][4]:
            Variable.mimue0[0][1]= Variable.mimue0[0][2]
            Variable.mimue0[1][1] = Variable.mimue0[1][2]
            Variable.mimue0[0][3] = Variable.mimue0[0][4]
            Variable.mimue0[1][3] = Variable.mimue0[1][4]
            Variable.mimue0[0][2] = (Variable.mimue0[0][1]+ Variable.mimue0[0][3]) / 2
        elif Variable.mimue0[1][1] < Variable.mimue0[1][3] - stbkepse5 and Variable.mimue0[1][1] >= 0:
            Variable.mimue0[0][1]= Variable.mimue0[0][0]
            Variable.mimue0[1][1] = Variable.mimue0[1][0]
            Variable.mimue0[0][3] = Variable.mimue0[0][2]
            Variable.mimue0[1][3] = Variable.mimue0[1][2]
            Variable.mimue0[0][2] = (Variable.mimue0[0][1]+ Variable.mimue0[0][3]) / 2
        elif Variable.mimue0[1][3] < Variable.mimue0[1][1] - stbkepse5 and Variable.mimue0[1][3] >= 0:
            Variable.mimue0[0][1]= Variable.mimue0[0][2]
            Variable.mimue0[1][1] = Variable.mimue0[1][2]
            Variable.mimue0[0][3] = Variable.mimue0[0][4]
            Variable.mimue0[1][3] = Variable.mimue0[1][4]
            Variable.mimue0[0][2] = (Variable.mimue0[0][1]+ Variable.mimue0[0][3]) / 2
        else:
            bEnd = True
        
        Variable.stbZerfmue0[2] = Variable.mimue0[0][2]
    else:
        if Variable.stbZsymm == True:
            Variable.mue_loop = False
        elif bEnd:
            if sum_mue0 >= 0:
                Variable.mue_loop = False
            else:
                Variable.stbZsymm = True
            
        elif Variable.mimue0[0][3] - Variable.mimue0[0][1]< stbkepse5:
            if sum_mue0 >= 0:
                Variable.mue_loop = False
            else:
                Variable.stbZerfmue0[2] = Variable.mimue0[0][3]
                bEnd = True
            
        else:
            if Variable.mimue0[1][2] < Variable.mimue0[1][3] - stbkepse5 and Variable.mimue0[1][2] >= 0:
                Variable.mimue0[0][3] = Variable.mimue0[0][2]
                Variable.mimue0[1][3] = Variable.mimue0[1][2]
                Variable.mimue0[0][2] = (Variable.mimue0[0][1]+ Variable.mimue0[0][3]) / 2
            else:
                Variable.mimue0[0][1]= Variable.mimue0[0][2]
                Variable.mimue0[1][1] = Variable.mimue0[1][2]
                Variable.mimue0[0][2] = (Variable.mimue0[0][1]+ Variable.mimue0[0][3]) / 2
            
            Variable.stbZerfmue0[2] = Variable.mimue0[0][2]
    # print(Smue0opt)


def SRissB():
    SgamC1()
    if Variable.stboRissP1 >= 1 or Variable.stboii >= 20:
        Gebrauch_R()
    if Variable.stboRissP1 >= 1 and stbfsig_s(Variable.stbZepssk[1]) > Variable.stboRissP1:
        SigVor_R()
    if Variable.stboQuer == 3 and (Variable.stbZmue0[1] > Variable.stbZerfmue0[1] + stbkepse5 or Variable.stbZmue0[2] > Variable.stbZerfmue0[2] + stbkepse5):
        Bruch_R()
    #print(SRissB)


def SgamC1():
    fnullC = [0,0,0,0]
    erfmue2 = [0,0,0]
    Variable.stbZiZ = 1
    SRechenWerteZ(1)
    if Variable.stbobminBew :
        vormue0_3 = max(Variable.stbovormue0[0], Variable.stbomue0Riss[0]) + max(Variable.stbovormue0[1], Variable.stbomue0Riss[1]) + max(Variable.stbovormue0[2], Variable.stbomue0Riss[2])
    else:
        vormue0_3 = Variable.stbovormue0[0] + Variable.stbovormue0[1] + Variable.stbovormue0[2]
    

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
    if Variable.stboQuer == 3 :
        Serfmue0_R()
        erfmue_0 = Variable.stbZerfmue0[1] + Variable.stbZerfmue0[2]
    
    if Variable.stboQuer == 3 :
        Variable.stbZmue0[0] = 0
        Variable.stbZmue0[1] = max(Variable.stbZerfmue0[1], Variable.stbovormue0[1])
        if Variable.stbosymmue0 == True:
            Variable.stbZmue0[2] = Variable.stbZmue0[1]
        else:
            Variable.stbZmue0[2] = max(Variable.stbZerfmue0[2], Variable.stbovormue0[2])
        
        if Variable.stboNd > stbkepse5 and Variable.stbZmue0[1] > (Variable.stbZerfmue0[1] + stbkepse7) and Variable.stbosymmue0 == False:
            if Variable.stboMd / Variable.stboNd < 0.5 - Variable.stbZ_H[1] / Variable.stboD:
                erfmue2[1] = Variable.stbZmue0[1]
                Serfmue2_R(erfmue2)
                Variable.stbZmue0[2] = max(erfmue2[2], Variable.stbZmue0[2])
        
    if bLastLoop :
        bLoop = False
    else:
        if Variable.stboNorm == 0 :
            if erfmue_0 < stbkepse7 :
                interpol = 0
            else:
                if Variable.stboQuer == 3 and (Variable.stbZmue0[1] > Variable.stbZerfmue0[1] + stbkepse5 or Variable.stbZmue0[2] > Variable.stbZerfmue0[2] + stbkepse5):
                    Bruch_R()
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

        if Variable.stboQuer == 3 :
            Serfmue0_R()
            erfmue_0 = Variable.stbZerfmue0[1] + Variable.stbZerfmue0[2]
        
        if Variable.stboQuer == 3 :
            Variable.stbZmue0[0] = 0
            Variable.stbZmue0[1] = max(Variable.stbZerfmue0[1], Variable.stbovormue0[1])
            if Variable.stbosymmue0 == True:
                Variable.stbZmue0[2] = Variable.stbZmue0[1]
            else:
                Variable.stbZmue0[2] = max(Variable.stbZerfmue0[2], Variable.stbovormue0[2])
            
            if Variable.stboNd > stbkepse5 and Variable.stbZmue0[1] > (Variable.stbZerfmue0[1] + stbkepse7) and Variable.stbosymmue0 == False:
                if Variable.stboMd / Variable.stboNd < 0.5 - Variable.stbZ_H[1] / Variable.stboD:
                    erfmue2[1] = Variable.stbZmue0[1]
                    Serfmue2_R(erfmue2)
                    Variable.stbZmue0[2] = max(erfmue2[2], Variable.stbZmue0[2])
                
        if bLastLoop :
            bLoop = False
        else:
            if Variable.stboNorm == 0 :
                if erfmue_0 < stbkepse7 :
                    interpol = 0
                else:
                    if Variable.stboQuer == 3 and (Variable.stbZmue0[1] > Variable.stbZerfmue0[1] + stbkepse5 or Variable.stbZmue0[2] > Variable.stbZerfmue0[2] + stbkepse5):
                        Bruch_R()
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
        print("sgamc1 lo")
        Variable.stbZbFehler = True
    #print(Variable.stbZeps_c)
    #print(SgamC1)
#############################K - requirements#######################################################
i2n = 9
def stbfphiAo():
    SRechenWerteZ(1)
    r1 = 1
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

def stbfphiAu():

    SRechenWerteZ(1)
    r1 = 1
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

def stbfKnbU():
    SRechenWerteZ(1)
    phiAo = stbfphiAo()
    phiAu = stbfphiAu()
    phiBo = phiAu
    phiBu = 0
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

def stbfKmbU():
    SRechenWerteZ(1)
    phiAo = stbfphiAo()
    phiAu = stbfphiAu()
    phiBo = phiAu
    phiBu = 0
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


#############################Getting into R things#################################################
def StB_R_MN(Norm , gam_c , gam_s , Md , Nd , Mk , Nk , DD , BB , HH_ , H__ , sym0 , vorAs1 , vorAs2 , f_ck , alpha , eps_cy , eps_cu , n2 , delt_S , delt_K , f_yk , f_tk , Es , eps_su , RissP1 , minBew ,  ii ) :

    mue0 = [0,0,0]

    stboNachweis = 1
    stboQuer = 3

    RechenWerte(Norm, gam_c, gam_s, Md, Nd, 0, Mk, Nk, DD, BB, HH_, H__, sym0, 0, 0, vorAs1, vorAs2, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, RissP1, minBew, 0, 0, 0, ii)
    if Variable.stbZbFehler : 
        print('Error')
    if Variable.stboNullSd :
        Variable.stbZerfmue0[1] = 0
        Variable.stbZerfmue0[2] = 0
        Variable.stbZmue0[1] = Variable.stbovormue0[1]
        Variable.stbZmue0[2] = Variable.stbovormue0[2]
        if Variable.stbobminBew :
            Variable.stbZmue0[1] = max(Variable.stbZmue0[1], Variable.stbomue0Riss[1])
            Variable.stbZmue0[2] = max(Variable.stbZmue0[2], Variable.stbomue0Riss[2])
    else:
        if Variable.stbobDruc[2] and Variable.stbovormue0[1] <= stbkepse7 and Variable.stbobminBew == False :
            Snue0_R()
            if Variable.stbZnue0 > 0 :
                Variable.stbZerfmue0[1] = 0
                Variable.stbZerfmue0[2] = 0
                Variable.stbZmue0[1] = 0
                Variable.stbZmue0[2] = 0
            
        else:
            Variable.stbZnue0 = -1
        if Variable.stbZnue0 < 0 :
            SRissB()

    if Variable.stbZbFehler :
        StB_R_Mn = 0
    elif Variable.stboii == 11 :
        StB_R_Mn = Variable.stbZepscd[1 + Variable.stboVMd]
    elif Variable.stboii == 12 :
        StB_R_Mn = Variable.stbZepscd[2 - Variable.stboVMd]
    elif Variable.stboii == 13 :
        if Variable.stbZmue0[1 + Variable.stboVMd] < stbkepse7 :
            StB_R_Mn = ""
        else:
            StB_R_Mn = Variable.stbZepssd[1 + Variable.stboVMd]
        
    elif Variable.stboii == 14 :
        if Variable.stbZmue0[2 - Variable.stboVMd] < stbkepse7 :
            StB_R_Mn = ""
        else:
            StB_R_Mn = Variable.stbZepssd[2 - Variable.stboVMd]
        
    elif Variable.stboii == 15 :
        StB_R_Mn = math.copysign(1,Md) * Variable.stbZRMd * 1000 * Variable.stboRB * Variable.stboD ** 2 * Variable.stbofck
    elif Variable.stboii == 16 :
        StB_R_Mn = Variable.stbZRNd * 1000 * Variable.stboRB * Variable.stboD * Variable.stbofck
    elif Variable.stboii == 17 :
        StB_R_Mn = 10000 * Variable.stbZmue0[1 + Variable.stboVMd] * Variable.stboRB * Variable.stboD * Variable.stbofck / Variable.stboftk
    elif Variable.stboii == 18 :
        StB_R_Mn = 10000 * Variable.stbZmue0[2 - Variable.stboVMd] * Variable.stboRB * Variable.stboD * Variable.stbofck / Variable.stboftk
    elif Variable.stboii == 19 :
        if Variable.stboNullSd :
            StB_R_Mn = 0
        else:
            if Variable.stbZmue0[1] + Variable.stbZmue0[2] < stbkepse7 :
                StB_R_Mn = Variable.stboNd / Variable.stbZRNd
            else:
                if vorAs1 < stbkepse7 and vorAs2 < stbkepse7 :
                    StB_R_Mn = max(Variable.stbZerfmue0[1] + Variable.stbZerfmue0[2], 0) / (Variable.stbZmue0[1] + Variable.stbZmue0[2])
                else:
                    mue0[1] = Variable.stbZmue0[1]
                    mue0[2] = Variable.stbZmue0[2]
                    StB_R_Mn = (StB_R_MN(Norm, gam_c, gam_s, Md, Nd, Mk, Nk,DD, BB, HH_, H__, sym0, 0, 0, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, 0, minBew, 17) + StB_R_MN(Norm, gam_c, gam_s, Md, Nd, Mk, Nk,DD, BB, HH_, H__, sym0, 0, 0, f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, 0, minBew, 18)) / 10000 / Variable.stboRB / Variable.stboD / Variable.stbofck * Variable.stboftk / (mue0[1] + mue0[2])
                
    elif Variable.stboii == 21 :
        StB_R_Mn = Variable.stbZepsck[1 + Variable.stboVMk]
    elif Variable.stboii == 22 :
        StB_R_Mn = Variable.stbZepsck[2 - Variable.stboVMk]
    elif Variable.stboii == 23 :
        if Variable.stbZmue0[1 + Variable.stboVMk] < stbkepse7 :
            StB_R_Mn = ""
        else:
            StB_R_Mn = Variable.stbZepssk[1 + Variable.stboVMk]
        
    elif Variable.stboii == 24 :
        if Variable.stbZmue0[2 - Variable.stboVMk] < stbkepse7 :
            StB_R_Mn = ""
        else:
            StB_R_Mn = Variable.stbZepssk[2 - Variable.stboVMk]
        
    elif Variable.stboii == 25 :
        StB_R_Mn = math.copysign(1,Mk) * Variable.stbZRMk * 1000 * Variable.stboRB * Variable.stboD ** 2 * Variable.stbofck
    elif Variable.stboii == 26 :
        StB_R_Mn = Variable.stbZRNk * 1000 * Variable.stboRB * Variable.stboD * Variable.stbofck
    elif Variable.stboii == 27 :
        if Variable.stbZmue0[1 + Variable.stboVMk] < stbkepse7 :
            StB_R_Mn = ""
        else:
            StB_R_Mn = stbfsig_s(Variable.stbZepssk[1 + Variable.stboVMk])
        
    elif Variable.stboii == 28 :
        if Variable.stbZmue0[2 - Variable.stboVMk] < stbkepse7 :
            StB_R_Mn = ""
        else:
            StB_R_Mn = stbfsig_s(Variable.stbZepssk[2 - Variable.stboVMk])
        
    else:
        StB_R_Mn = ""
    return StB_R_Mn

def StB_R_Q(Norm , gam_c , gam_s , Md , Nd , Qd , DD , BB , HH_ , H__ , vorAs1 , vorAs2 , f_ck , alpha , eps_cy , eps_cu , n2 , delt_S , delt_K , f_yk , f_tk , Es , eps_su ,TauP1 , TauP2 , TauP3 , ii ) :
    stboNachweis = 2
    stboQuer = 3

    RechenWerte(Norm, gam_c, gam_s, Md, Nd, Qd, 0, 0, DD, BB, HH_, H__, False, 0, 0, vorAs1, vorAs2,f_ck, alpha, eps_cy, eps_cu, n2, delt_S, delt_K, f_yk, f_tk, Es, eps_su, 0, 0, TauP1, TauP2, TauP3, ii)
    if Variable.stbZbFehler : 
        print("error")

    if not Variable.stboNullSd :
        BruchC1S1()
    

    if Variable.stboNorm == 0 :
        QuerBemessN0()
    elif Variable.stboNorm > 0 :
        QuerBemessN123()
    

    if Variable.stbZbFehler :
        StB_R_Q = 0
    elif Variable.stboii == 11 :
        if Variable.stbZNucs[0] > -stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = Variable.stbZNucs[0] * 1000 * Variable.stboRB * Variable.stboD * Variable.stbofck
        
    elif Variable.stboii == 12 :
        if Variable.stbZNucs[0] > -stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = math.copysign(1,Md) * Variable.stbZzi[0] * 1000
        
    elif Variable.stboii == 13 :
        if Variable.stbZNucs[1] < stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = Variable.stbZNucs[1] * 1000 * Variable.stboRB * Variable.stboD * Variable.stbofck
        
    elif Variable.stboii == 14 :
        if Variable.stbZNucs[1] < stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = math.copysign(1,Md) * Variable.stbZzi[1] * 1000
        
    elif Variable.stboii == 15 :
        if Variable.stbZNucs[2] > -stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = Variable.stbZNucs[2] * 1000 * Variable.stboRB * Variable.stboD * Variable.stbofck
        
    elif Variable.stboii == 16 :
        if Variable.stbZNucs[2] > -stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = math.copysign(1,Md) * Variable.stbZzi[2] * 1000
        
    elif Variable.stboii == 17 :
        if Variable.stbZNucs[3] < stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = Variable.stbZNucs[3] * 1000 * Variable.stboRB * Variable.stboD * Variable.stbofck
        
    elif Variable.stboii == 18 :
        if Variable.stbZNucs[3] < stbkepse7 :
            StB_R_Q = ""
        else:
            StB_R_Q = Variable.stbZzi[3] * 1000
        
    elif Variable.stboii == 19 :
        StB_R_Q = Variable.stbZerfas
    elif Variable.stboii == 20 :
        if Variable.stboNorm == 0 :
            StB_R_Q = Variable.stbZtau0
        else:
            StB_R_Q = Variable.stbZminas
        
    elif Variable.stboii == 21 :
        if Variable.stboNorm == 0 :
            StB_R_Q = Variable.stbotau012
        else:
            StB_R_Q = Variable.stbZVRdc * 1000
        
    elif Variable.stboii == 22 :
        if Variable.stboNorm == 0 :
            StB_R_Q = Variable.stbotau02
        else:
            if Variable.stbZmue0[1] < stbkepse7 :
                StB_R_Q = Variable.stbZtaucp
            else:
                StB_R_Q = Variable.stbZVRdmax * 1000
            
        
    elif Variable.stboii == 23 :
        if Variable.stboNorm == 0 :
            StB_R_Q = Variable.stbotau03
        else:
            if Variable.stbZmue0[1] < stbkepse7 :
                StB_R_Q = Variable.stbZfcvd
            else:
                StB_R_Q = Variable.stbZcottheta
            
        
    else:
        StB_R_Q = ""
    return StB_R_Q

def Snue0_R():
    dehn = [0,0,0,0] 
    f_null= [0,1,0,0]

    for it_dehn in range(1,stbkitmax):
        if it_dehn == 2 or abs(f_null[1]) > stbkepse7:
            Sitdehn0(dehn, f_null, it_dehn)
            Sdehnepscs(dehn[1])
            n_bU = stbfRnbU()
            m_bU = stbfRmbU()
            f_null[1] = Variable.stboMd * n_bU - Variable.stboNd * m_bU
        else:
            break

    if it_dehn == stbkitmax : 
        Variable.stbZbFehler = True

    Variable.stbZnue0 = (abs(n_bU) + m_bU) / (abs(Variable.stboNd) + Variable.stboMd)
    if Variable.stbZnue0 >= Variable.stbogamC[0] - stbkepse5 and Variable.stbZbFehler == False :
        Variable.stbZgamC[1] = Variable.stbogamC[0]
        Variable.stbZgamS[1] = Variable.stbogamS[0]
        Variable.stbZRNd = n_bU / Variable.stbZgamC[1]
        Variable.stbZRMd = m_bU / Variable.stbZgamC[1]
        if Variable.stboii >= 20 :
            Gebrauch_R()
        
    else:
        Variable.stbZnue0 = -Variable.stbZnue0
    


def stbfyAo() :
    SRechenWerteZ(1)
    D1 = 1
    if Variable.stbZeps_c[1] < 0 :
        if Variable.stbZeps_c[2] < 0 or abs(Variable.stbZeps_c[1] - Variable.stbZeps_c[2]) < stbkepse7 :
            stbfyAo = D1 / 2
        else:
            stbfyAo = (Variable.stbZeps_c[1] + Variable.stbZeps_c[2]) / 2 * D1 / (Variable.stbZeps_c[1] - Variable.stbZeps_c[2])
        
    else:
        stbfyAo = -D1 / 2
    return stbfyAo


def stbfyAu() :
    SRechenWerteZ(1)
    D1 = 1
    if Variable.stbZeps_c[1] < -Variable.stboepscy :
        if abs(Variable.stbZeps_c[1] - Variable.stbZeps_c[2]) < stbkepse7 :
            stbfyAu = D1 / 2
        else:
            stbfyAu = (Variable.stboepscy + (Variable.stbZeps_c[1] + Variable.stbZeps_c[2]) / 2) * D1 / (Variable.stbZeps_c[1] - Variable.stbZeps_c[2])  
    else:
        stbfyAu = -D1 / 2
    return stbfyAu


def stbfRnbU(): 
    SRechenWerteZ(1)
    yAo = stbfyAo()
    yAu = stbfyAu()
    yBo = yAu
    yBu = -0.5
    if Variable.stbZeps_c[1] < 0 :
        m1 = -(Variable.stbZeps_c[2] + Variable.stbZeps_c[1]) / Variable.stboepscy / 2
        m2 = -(Variable.stbZeps_c[2] - Variable.stbZeps_c[1]) / Variable.stboepscy
        if abs(yAo - yAu) < stbkepse7 :
            nAbU = 0
        elif abs(m2) < stbkepse7 :
            if m1 <= 0 :
                nAbU = 0
            elif m1 >= 1 :
                nAbU = -1
            else:
                nAbU = -1 * (1 - (1 - m1) ** Variable.stbon2)
            
        else:
            nAbU = (abs(1 - m1 - m2 * yAu) ** (Variable.stbon2 + 1) - abs(1 - m1 - m2 * yAo) ** (Variable.stbon2 + 1)) / m2 / (Variable.stbon2 + 1) + (yAu - yAo)
        
        nBbU = yBu - yBo
    else:
        nAbU = 0
        nBbU = 0
    stbfRnbU = nAbU + nBbU
    return stbfRnbU

def stbfRmbU(): 
    SRechenWerteZ(1)
    yAo = stbfyAo()
    yAu = stbfyAu()
    yBo = yAu
    yBu = -0.5
    if Variable.stbZeps_c[1] < 0 :
        m1 = -(Variable.stbZeps_c[2] + Variable.stbZeps_c[1]) / Variable.stboepscy / 2
        m2 = -(Variable.stbZeps_c[2] - Variable.stbZeps_c[1]) / Variable.stboepscy
        if abs(yAo - yAu) < stbkepse7 :
            mAbU = 0
        elif abs(m2) < stbkepse7 :
            mAbU = 0
        else:
            mAbU = (abs(1 - m1 - m2 * yAo) ** (Variable.stbon2 + 2) - abs(1 - m1 - m2 * yAu) ** (Variable.stbon2 + 2)) / m2 ** 2 / (Variable.stbon2 + 2) + (abs(1 - m1 - m2 * yAo) ** (Variable.stbon2 + 1) - abs(1 - m1 - m2 * yAu) ** (Variable.stbon2 + 1)) / m2 ** 2 / (Variable.stbon2 + 1) * (m1 - 1) - (yAo ** 2 - yAu ** 2) / 2 
        mBbU = (yBu ** 2 - yBo ** 2) / 2
    else:
        mAbU = 0
        mBbU = 0
    return mAbU + mBbU

def stbfRneU1(): 
    SRechenWerteZ(1)
    if abs(Variable.stbZeps_s[1]) <= Variable.stboepssy :
        stbfRneU1 = Variable.stbZeps_s[1] / Variable.stboepssy * Variable.stbofyk / Variable.stboftk
    else:
        stbfRneU1 = math.copysign(1,Variable.stbZeps_s[1]) * (Variable.stbofyk / Variable.stboftk + (1 - Variable.stbofyk / Variable.stboftk) * (abs(Variable.stbZeps_s[1]) - Variable.stboepssy) / (Variable.stboepssu - Variable.stboepssy))
    return stbfRneU1


def stbfRmeU1(): 
    SRechenWerteZ(1)
    stbfRmeU1 = stbfRneU1() * (Variable.stboD / 2 - Variable.stbZ_H[1]) / Variable.stboD
    return stbfRmeU1

def stbfRneU2(): 
    SRechenWerteZ(1)
    if abs(Variable.stbZeps_s[2]) <= Variable.stboepssy :
        stbfRneU2 = Variable.stbZeps_s[2] / Variable.stboepssy * Variable.stbofyk / Variable.stboftk
    else:
        stbfRneU2 = math.copysign(1,Variable.stbZeps_s[2]) * (Variable.stbofyk / Variable.stboftk + (1 - Variable.stbofyk / Variable.stboftk) * (abs(Variable.stbZeps_s[2]) - Variable.stboepssy) / (Variable.stboepssu - Variable.stboepssy))
    return stbfRneU2


def stbfRmeU2(): 
    SRechenWerteZ(1)
    stbfRmeU2 = -stbfRneU2() * (Variable.stboD / 2 - Variable.stbZ_H[2]) / Variable.stboD
    return stbfRmeU2

def Serfmue2_R(erfmue2):
    n_eU = [0,0,0]
    m_eU = [0,0,0]
    Sdehnepscs(1)

    n_bU = stbfRnbU()
    m_bU = stbfRmbU()

    n_eU[1] = stbfRneU1()
    m_eU[1] = stbfRmeU1()
    n_eU[2] = stbfRneU2()
    m_eU[2] = stbfRmeU2()

    if abs(m_eU[2]) > stbkepse7 :
        erfmue2[2] = Variable.stbZgamS[1] * (Variable.stboMd - m_bU / Variable.stbZgamC[1] - erfmue2[1] * m_eU[1] / Variable.stbZgamS[1]) / m_eU[2]
    else:
        erfmue2[2] = 1 / stbkepse7

    Variable.stbZRNd = n_bU / Variable.stbZgamC[1] + erfmue2[1] * n_eU[1] / Variable.stbZgamS[1] + erfmue2[2] * n_eU[2] / Variable.stbZgamS[1]
    Variable.stbZRMd = m_bU / Variable.stbZgamC[1] + erfmue2[1] * m_eU[1] / Variable.stbZgamS[1] + erfmue2[2] * m_eU[2] / Variable.stbZgamS[1]

def Serfmue0_R():
    n_eU = [0,0,0]
    m_eU = [0,0,0]
    dehn = [0,0,0,0] 

    f_null = [0,1,0,0] 

    it_mue = 1
    Variable.stbZsymm = True 
    Variable.mue_loop = False
    it_dehn = 1
    while (((it_dehn == 1 or (Variable.stboNd >= stbkepse5 or Variable.stboMd >= stbkepse5)) or (it_dehn == 2 and (Variable.stboNd <= -stbkepse5 or Variable.stboMd >= stbkepse5)) or it_dehn == 3 or abs(f_null[1]) > stbkepse7)) and it_dehn < stbkitmax:
        it_dehn = it_dehn + 1
        if it_dehn == 3 :
            dehn[3] = dehn[1]
            f_null[3] = f_null[1]
            if Variable.stbZsymm :
                dehn[1] = Variable.stbodehnkrit[1]
            else:
                dehn[1] = Variable.stbodehnkrit[2] - stbkepse3
            
        elif it_dehn == 4 and Variable.stbZsymm == False :
            fnull2 = f_null[1]
            dehn[1] = Variable.stbodehnkrit[2] + stbkepse3
        elif it_dehn == 5 and Variable.stbZsymm == False :
            fnull3 = f_null[1]
            if fnull2 * f_null[2] < 0 :
                dehn[3] = Variable.stbodehnkrit[2] - stbkepse3
                f_null[3] = fnull2
                dehn[1] = (dehn[2] + dehn[3]) / 2
            elif fnull3 * f_null[3] < 0 :
                dehn[2] = Variable.stbodehnkrit[2] + stbkepse3
                f_null[2] = fnull3
                dehn[1] = (dehn[2] + dehn[3]) / 2
            else:
                dehn[1] = Variable.stbodehnkrit[3]
            
        else:
            Sitdehn(dehn, f_null, it_dehn)
        
        
        Sdehnepscs(dehn[1])
        n_bU = stbfRnbU()
        m_bU = stbfRmbU()

        n_eU[1] = stbfRneU1()
        m_eU[1] = stbfRmeU1()
        n_eU[2] = stbfRneU2()
        m_eU[2] = stbfRmeU2()
        if Variable.stbZsymm :
            if abs(n_eU[1] + n_eU[2] + m_eU[1] + m_eU[2]) > stbkepse7 :
                Variable.stbZerfmue0[1] = Variable.stbZgamS[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] + Variable.stboMd - m_bU / Variable.stbZgamC[1]) / (n_eU[1] + n_eU[2] + m_eU[1] + m_eU[2])
            else:
                Variable.stbZerfmue0[1] = 1 / stbkepse7
            
            Variable.stbZerfmue0[2] = Variable.stbZerfmue0[1]
            f_null[1] = (m_eU[1] + m_eU[2]) * (Variable.stboNd - n_bU / Variable.stbZgamC[1]) - (n_eU[1] + n_eU[2]) * (Variable.stboMd - m_bU / Variable.stbZgamC[1])

        else:

            if abs(n_eU[1] + m_eU[1]) > stbkepse7 :
                Variable.stbZerfmue0[1] = Variable.stbZgamS[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1] + Variable.stboMd - m_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * m_eU[2] / Variable.stbZgamS[1]) / (n_eU[1] + m_eU[1])
            else:
                Variable.stbZerfmue0[1] = 1 / stbkepse7
            
            f_null[1] = m_eU[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1]) - n_eU[1] * (Variable.stboMd - m_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * m_eU[2] / Variable.stbZgamS[1])
    if Variable.stbZsymm and (it_dehn == stbkitmax or Variable.stbZerfmue0[1] < 0) and abs(Variable.stboNd) > stbkepse5 :
        if Variable.stboNd < -stbkepse5 and abs(Variable.stboeNd) < 0.5 - max(Variable.stboH[1], Variable.stboH[2]) / Variable.stboD :
            dehn[1] = -1
            bHlp = True
        elif Variable.stboNd > stbkepse5 and Variable.stboeNd < 0.5 - Variable.stbZ_H[1] / Variable.stboD :
            dehn[1] = 1
            bHlp = True
        else:
            bHlp = False
        
        if bHlp :
            Sdehnepscs(dehn[1])
            n_bU = stbfKnbU()
            m_bU = stbfKmbU()
            n_eU[1] = stbfRneU1()
            m_eU[1] = stbfRmeU1()
            n_eU[2] = stbfRneU2()
            m_eU[2] = stbfRmeU2()
            if abs(m_eU[1]) < stbkepse7 :
                Variable.stbZerfmue0[2] = (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[2] * Variable.stbZgamS[1]
                Variable.stbZerfmue0[1] = (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1]) / n_eU[1] * Variable.stbZgamS[1]
            elif abs(m_eU[2]) < stbkepse7 :
                Variable.stbZerfmue0[1] = (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[1] * Variable.stbZgamS[1]
                Variable.stbZerfmue0[2] = (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[1] * n_eU[1] / Variable.stbZgamS[1]) / n_eU[2] * Variable.stbZgamS[1]
            else:
                Variable.stbZerfmue0[2] = ((Variable.stboNd - n_bU / Variable.stbZgamC[1]) / n_eU[1] - (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[1]) * Variable.stbZgamS[1] / (n_eU[2] / n_eU[1] - m_eU[2] / m_eU[1])
                Variable.stbZerfmue0[1] = ((Variable.stboNd - n_bU / Variable.stbZgamC[1]) / n_eU[2] - (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[2]) * Variable.stbZgamS[1] / (n_eU[1] / n_eU[2] - m_eU[1] / m_eU[2])
            
            if abs(Variable.stbZmue0[1] - Variable.stbZmue0[2]) < stbkepse7 :
                Variable.stbZsymm = True
            else:
                Variable.stbZsymm = False
    Smue0opt(it_mue, Variable.mue_loop)
    while Variable.mue_loop and it_mue < stbkitmax:
        it_mue = it_mue + 1
        it_dehn = 1
        while (((it_dehn == 1 or (Variable.stboNd >= stbkepse5 or Variable.stboMd >= stbkepse5)) or (it_dehn == 2 and (Variable.stboNd <= -stbkepse5 or Variable.stboMd >= stbkepse5)) or it_dehn == 3 or abs(f_null[1]) > stbkepse7)) and it_dehn < stbkitmax:
            it_dehn = it_dehn + 1
            if it_dehn == 3 :
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
                if Variable.stbZsymm :
                    dehn[1] = Variable.stbodehnkrit[1]
                else:
                    dehn[1] = Variable.stbodehnkrit[2] - stbkepse3
                
            elif it_dehn == 4 and Variable.stbZsymm == False :
                fnull2 = f_null[1]
                dehn[1] = Variable.stbodehnkrit[2] + stbkepse3
            elif it_dehn == 5 and Variable.stbZsymm == False :
                fnull3 = f_null[1]
                if fnull2 * f_null[2] < 0 :
                    dehn[3] = Variable.stbodehnkrit[2] - stbkepse3
                    f_null[3] = fnull2
                    dehn[1] = (dehn[2] + dehn[3]) / 2
                elif fnull3 * f_null[3] < 0 :
                    dehn[2] = Variable.stbodehnkrit[2] + stbkepse3
                    f_null[2] = fnull3
                    dehn[1] = (dehn[2] + dehn[3]) / 2
                else:
                    dehn[1] = Variable.stbodehnkrit[3]
                
            else:
                Sitdehn(dehn, f_null, it_dehn)
            
            
            Sdehnepscs(dehn[1])
            n_bU = stbfRnbU()
            m_bU = stbfRmbU()

            n_eU[1] = stbfRneU1()
            m_eU[1] = stbfRmeU1()
            n_eU[2] = stbfRneU2()
            m_eU[2] = stbfRmeU2()
            if Variable.stbZsymm :
                if abs(n_eU[1] + n_eU[2] + m_eU[1] + m_eU[2]) > stbkepse7 :
                    Variable.stbZerfmue0[1] = Variable.stbZgamS[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] + Variable.stboMd - m_bU / Variable.stbZgamC[1]) / (n_eU[1] + n_eU[2] + m_eU[1] + m_eU[2])
                else:
                    Variable.stbZerfmue0[1] = 1 / stbkepse7
                
                Variable.stbZerfmue0[2] = Variable.stbZerfmue0[1]
                f_null[1] = (m_eU[1] + m_eU[2]) * (Variable.stboNd - n_bU / Variable.stbZgamC[1]) - (n_eU[1] + n_eU[2]) * (Variable.stboMd - m_bU / Variable.stbZgamC[1])

            else:

                if abs(n_eU[1] + m_eU[1]) > stbkepse7 :
                    Variable.stbZerfmue0[1] = Variable.stbZgamS[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1] + Variable.stboMd - m_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * m_eU[2] / Variable.stbZgamS[1]) / (n_eU[1] + m_eU[1])
                else:
                    Variable.stbZerfmue0[1] = 1 / stbkepse7
                
                f_null[1] = m_eU[1] * (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1]) - n_eU[1] * (Variable.stboMd - m_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * m_eU[2] / Variable.stbZgamS[1])
        if Variable.stbZsymm and (it_dehn == stbkitmax or Variable.stbZerfmue0[1] < 0) and abs(Variable.stboNd) > stbkepse5 :
            if Variable.stboNd < -stbkepse5 and abs(Variable.stboeNd) < 0.5 - max(Variable.stboH[1], Variable.stboH[2]) / Variable.stboD :
                dehn[1] = -1
                bHlp = True
            elif Variable.stboNd > stbkepse5 and Variable.stboeNd < 0.5 - Variable.stbZ_H[1] / Variable.stboD :
                dehn[1] = 1
                bHlp = True
            else:
                bHlp = False
            
            if bHlp :
                Sdehnepscs(dehn[1])
                n_bU = stbfKnbU()
                m_bU = stbfKmbU()
                n_eU[1] = stbfRneU1()
                m_eU[1] = stbfRmeU1()
                n_eU[2] = stbfRneU2()
                m_eU[2] = stbfRmeU2()
                if abs(m_eU[1]) < stbkepse7 :
                    Variable.stbZerfmue0[2] = (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[2] * Variable.stbZgamS[1]
                    Variable.stbZerfmue0[1] = (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1]) / n_eU[1] * Variable.stbZgamS[1]
                elif abs(m_eU[2]) < stbkepse7 :
                    Variable.stbZerfmue0[1] = (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[1] * Variable.stbZgamS[1]
                    Variable.stbZerfmue0[2] = (Variable.stboNd - n_bU / Variable.stbZgamC[1] - Variable.stbZerfmue0[1] * n_eU[1] / Variable.stbZgamS[1]) / n_eU[2] * Variable.stbZgamS[1]
                else:
                    Variable.stbZerfmue0[2] = ((Variable.stboNd - n_bU / Variable.stbZgamC[1]) / n_eU[1] - (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[1]) * Variable.stbZgamS[1] / (n_eU[2] / n_eU[1] - m_eU[2] / m_eU[1])
                    Variable.stbZerfmue0[1] = ((Variable.stboNd - n_bU / Variable.stbZgamC[1]) / n_eU[2] - (Variable.stboMd - m_bU / Variable.stbZgamC[1]) / m_eU[2]) * Variable.stbZgamS[1] / (n_eU[1] / n_eU[2] - m_eU[1] / m_eU[2])
                
                if abs(Variable.stbZmue0[1] - Variable.stbZmue0[2]) < stbkepse7 :
                    Variable.stbZsymm = True
                else:
                    Variable.stbZsymm = False
        Smue0opt(it_mue, Variable.mue_loop)
        if it_mue == stbkitmax : 
            Variable.stbZbFehler = True

    if Variable.stbobminBew and ((Variable.stbZerfmue0[1] <= Variable.stbomue0Riss[1] or Variable.stbZerfmue0[2] <= Variable.stbomue0Riss[2]) and (Variable.stbomue0Riss[1] > 20*stbkepse3 and Variable.stbomue0Riss[2] > 20*stbkepse3)) :
        Variable.stbZerfmue0[1] = Variable.stbomue0Riss[1]
        Variable.stbZerfmue0[2] = Variable.stbomue0Riss[2]
        Variable.stbZmue0[1] = Variable.stbZerfmue0[1]
        Variable.stbZmue0[2] = Variable.stbZerfmue0[2]
        Bruch_R()
    else:
        Variable.stbZRNd = n_bU / Variable.stbZgamC[1] + Variable.stbZerfmue0[1] * n_eU[1] / Variable.stbZgamS[1] + Variable.stbZerfmue0[2] * n_eU[2] / Variable.stbZgamS[1]
        Variable.stbZRMd = m_bU / Variable.stbZgamC[1] + Variable.stbZerfmue0[1] * m_eU[1] / Variable.stbZgamS[1] + Variable.stbZerfmue0[2] * m_eU[2] / Variable.stbZgamS[1]
    Variable.mimue0 = [[0,0,0,0,0],[0,0,0,0,0]]
    # print(Serfmue0_R)
    #print(Variable.stbZeps_c)
    


def Bruch_R():
    n_eU = [0,0,0]
    m_eU = [0,0,0]
    dehn = [0,0,0,0] 
    f_null = [0,0,0,0] 
    Variable.stbZiZ = 1

    eZug = Variable.stboeNd - stbfeBew()
    if Variable.stboNd < -stbkepse5 and abs(Variable.stboeNd) < stbkepse7 and (Variable.stbZmue0[1] + Variable.stbZmue0[2] < stbkepse7 or (Variable.stbobHkrit == False and abs(Variable.stbZmue0[1] - Variable.stbZmue0[2]) < stbkepse7)) :
        itmin = 0
    elif Variable.stboNd > stbkepse5 and (abs(eZug) < stbkepse7 or Variable.stboeNd < 0.5 - Variable.stbZ_H[1] / Variable.stboD) :
        itmin = 1
    else:
        itmin = 2

    dehnkrit = Variable.stboepscu / (Variable.stboepscu + Variable.stboepssu) - stbkepse5

    for it_dehn in range(0,stbkitmax):
        if it_dehn <= itmin or it_dehn == 3 or abs(f_null[1]) > stbkepse5:
            if it_dehn == 3 :
                dehn[3] = dehn[1]
                f_null[3] = f_null[1]
                dehn[1] = dehnkrit
            else:
                Sitdehn(dehn, f_null, it_dehn)
            Sdehnepscs(dehn[1])
            n_bU = stbfRnbU()
            m_bU = stbfRmbU()
            n_i = n_bU / Variable.stbZgamC[1]
            m_i = m_bU / Variable.stbZgamC[1]
            n_eU[1] = stbfRneU1()
            m_eU[1] = stbfRmeU1()
            n_i = n_i + Variable.stbZmue0[1] * n_eU[1] / Variable.stbZgamS[1]
            m_i = m_i + Variable.stbZmue0[1] * m_eU[1] / Variable.stbZgamS[1]
            n_eU[2] = stbfRneU2()
            m_eU[2] = stbfRmeU2()
            n_i = n_i + Variable.stbZmue0[2] * n_eU[2] / Variable.stbZgamS[1]
            m_i = m_i + Variable.stbZmue0[2] * m_eU[2] / Variable.stbZgamS[1]
            f_null[1] = Variable.stboMd * n_i - Variable.stboNd * m_i
        else:
            break

    if it_dehn == stbkitmax :
         Variable.stbZbFehler = True

    Variable.stbZRNd = n_bU / Variable.stbZgamC[1] + Variable.stbZmue0[1] * n_eU[1] / Variable.stbZgamS[1] + Variable.stbZmue0[2] * n_eU[2] / Variable.stbZgamS[1]
    Variable.stbZRMd = m_bU / Variable.stbZgamC[1] + Variable.stbZmue0[1] * m_eU[1] / Variable.stbZgamS[1] + Variable.stbZmue0[2] * m_eU[2] / Variable.stbZgamS[1]
    
    # print(Bruch_R)


def Gebrauch_R():
    eps0 = [0,0,0] 
    eps1= [0,0,0,0]
    eps2 = [0,0,0,0] 
    fnull_n= [0,0,0,0] 
    fnull_m = [0,0,0,0] 
    Variable.stbZiZ = 2
    if abs(Variable.stboNk) < stbkepse5 :
        eps0[1] = 0
    elif Variable.stboNk < 0 :
        it_n = 1
        eps2[1] = 0
        Variable.stbZepssk[1] = eps2[1]
        Variable.stbZepsck[1] = eps2[1]
        Variable.stbZepssk[2] = eps2[1]
        Variable.stbZepsck[2] = eps2[1]
        Variable.stbZRNk = stbfalpha() * stbfRnbU() + Variable.stbZmue0[1] * stbfRneU1() + Variable.stbZmue0[2] * stbfRneU2()
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
            Variable.stbZRNk = stbfalpha() * stbfRnbU() + Variable.stbZmue0[1] * stbfRneU1() + Variable.stbZmue0[2] * stbfRneU2()
            fnull_n[1] = Variable.stboNk - Variable.stbZRNk
        if it_n == stbkitmax : 
            Variable.stbZbFehler = True
        eps0[1] = eps2[1]                                                   
    else:
        Nkgr = Variable.stbZmue0[1] + Variable.stbZmue0[2]                                  
        if Variable.stboNk <= (Variable.stbZmue0[1] + Variable.stbZmue0[2]) * Variable.stbofyk / Variable.stboftk :
            eps0[1] = Variable.stboepssy * Variable.stboNk / (Nkgr * Variable.stbofyk / Variable.stboftk)       
        else:
            eps0[1] = Variable.stboepssy + (Variable.stboepssu - Variable.stboepssy) * (Variable.stboNk - (Variable.stbZmue0[1] + Variable.stbZmue0[2]) * Variable.stbofyk / Variable.stboftk) / (Variable.stbZnue0 * (1 - Variable.stbofyk / Variable.stboftk))            
        Variable.stbZepssk[1] = eps0[1]
        Variable.stbZepsck[1] = eps0[1]
        Variable.stbZepssk[2] = eps0[1]
        Variable.stbZepsck[2] = eps0[1]
    
    eps0[2] = eps0[1]
    Variable.stbZRMk = stbfalpha() * stbfRmbU() + Variable.stbZmue0[1] * stbfRmeU1() + Variable.stbZmue0[2] * stbfRmeU2()
    if Variable.stbZRMk > Variable.stboMk + stbkepse5 :
        if Variable.stboNk < 0 :
            eps0[2] = eps0[2] / 2
        else:
            eps0[1] = eps0[1] / 2

    it_m = 1
    it_ult = 1
    eps1[1] = eps0[1]
    it_n = 1
    eps2[1] = eps0[2]
    Variable.stbZepssk[1] = eps1[1]
    Variable.stbZepsck[1] = eps2[1]
    Sepsc2s2()
    Variable.stbZRNk = stbfalpha() * stbfRnbU() + Variable.stbZmue0[1] * stbfRneU1() + Variable.stbZmue0[2] * stbfRneU2()
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
        Variable.stbZRNk = stbfalpha() * stbfRnbU() + Variable.stbZmue0[1] * stbfRneU1() + Variable.stbZmue0[2] * stbfRneU2()
        fnull_n[1] = Variable.stboNk - Variable.stbZRNk
    Variable.stbZRMk = stbfalpha() * stbfRmbU() + Variable.stbZmue0[1] * stbfRmeU1() + Variable.stbZmue0[2] * stbfRmeU2()
    fnull_m[1] = Variable.stboMk - Variable.stbZRMk
    while abs(fnull_m[1]) > stbkepse5 and it_ult < stbkitmax:
        it_m = it_m + 1
        it_ult = it_ult + 1
        if it_m == 2 :
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
            
        else:
            if fnull_m[1] * fnull_m[2] < 0 :
                fnull_m[3] = fnull_m[1]
                eps1[3] = eps1[1]
            else:
                fnull_m[2] = fnull_m[1]
                eps1[2] = eps1[1]
            
            eps1[1] = (eps1[2] + eps1[3]) / 2
        
        it_n = 1
        eps2[1] = eps0[2]
        Variable.stbZepssk[1] = eps1[1]
        Variable.stbZepsck[1] = eps2[1]
        Sepsc2s2()
        Variable.stbZRNk = stbfalpha() * stbfRnbU() + Variable.stbZmue0[1] * stbfRneU1() + Variable.stbZmue0[2] * stbfRneU2()
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
            Variable.stbZRNk = stbfalpha() * stbfRnbU() + Variable.stbZmue0[1] * stbfRneU1() + Variable.stbZmue0[2] * stbfRneU2()
            fnull_n[1] = Variable.stboNk - Variable.stbZRNk
        Variable.stbZRMk = stbfalpha() * stbfRmbU() + Variable.stbZmue0[1] * stbfRmeU1() + Variable.stbZmue0[2] * stbfRmeU2()
        fnull_m[1] = Variable.stboMk - Variable.stbZRMk
    if it_ult == stbkitmax : 
        Variable.stbZbFehler = True
    # print(Gebrauch_R)

def SigVor_R():
    mue01 = [0,0,0,0]
    eps2= [0,0,0,0]
    fnull_n= [0,0,0,0]
    fnull_m= [0,0,0,0]

    Variable.stbZiZ = 2

    if Variable.stboRissP1 <= Variable.stbofyk + 0.1 :
        Variable.stbZepssk[1] = Variable.stboRissP1 / (Variable.stbofyk / Variable.stboepssy)
    else:
        Variable.stbZepssk[1] = Variable.stboepssy + (Variable.stboepssu - Variable.stboepssy) * (Variable.stboRissP1 - Variable.stbofyk) / (Variable.stboftk - Variable.stbofyk)

    if Variable.stboNk < stbkepse5 :
        eps0 = 0
    else:
        eps0 = Variable.stbZepssk[1]

    if Variable.stboNk > stbkepse5 and abs(Variable.stboeNk - stbfeBew()) < stbkepse7 :
        Variable.stbZsymm = True
        Variable.stbZepsck[1] = Variable.stbZepssk[1]
        Sepsc2s2()
        mue01[1] = Variable.stboNk * Variable.stboftk / Variable.stboRissP1 / 2
        mue02 = mue01[1]
        Variable.stbZRNk = mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
        Variable.stbZRMk = mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()

        Variable.stbZmue0[1] = mue01[1]
        Variable.stbZmue0[2] = mue02

    elif Variable.stboNk > stbkepse5 and Variable.stboeNk < 0.5 - Variable.stbZ_H[1] / Variable.stboD  and (Variable.stbobHkrit or Variable.stbZsymm == False) :
        mue02 = Variable.stbZmue0[2]
        Variable.stbZepsck[1] = Variable.stbZepssk[1]
        Sepsc2s2()
        mue01[1] = Variable.stboNk * Variable.stboftk / Variable.stboRissP1 - mue02
        RMk0 = mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
        Variable.stbZepsck[1] = 0
        Sepsc2s2()
        mue01[1] = (Variable.stboNk - mue02 * stbfRneU2()) / stbfRneU1()
        RMk1 = mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
        if Variable.stboMk <= RMk0 :
            Variable.stbZepsck[1] = Variable.stbZepssk[1]
            Sepsc2s2()
            Det0 = stbfRmeU2() - stbfRmeU1()
            Det1 = Variable.stboNk * Variable.stboftk / Variable.stboRissP1 * stbfRmeU2() - Variable.stboMk
            Det2 = Variable.stboMk - Variable.stboNk * Variable.stboftk / Variable.stboRissP1 * stbfRmeU1()
            mue01[1] = Det1 / Det0
            mue02 = Det2 / Det0
            Variable.stbZRMk = mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
            Variable.stbZRNk = mue01[1] * stbfRneU1() + mue02 * stbfRneU2()

            Variable.stbZmue0[1] = mue01[1]
            Variable.stbZmue0[2] = mue02
        elif Variable.stboMk <= RMk1 :
            it_m = 1
            eps2[1] = eps0
            Variable.stbZepsck[1] = eps2[1]
            Sepsc2s2()
            it_n = 1
            it_ult = 1
            mue01[1] = Variable.stbZmue0[1]  
            Variable.stbZRNk = mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
            fnull_n[1] = Variable.stboNk - Variable.stbZRNk
            while abs(fnull_n[1]) > stbkepse5 and it_ult < stbkitmax:
                it_n = it_n + 1
                it_ult = it_ult + 1
                if it_n == 2 :
                    fnull_n[2] = fnull_n[1]
                    mue01[2] = mue01[1]
                    mue01[1] = 2 * mue01[1]
                elif it_n == 3 :
                    if fnull_n[1] * fnull_n[2] > 0 :
                        it_n = 2
                        fnull_n[2] = fnull_n[1]
                        mue01[2] = mue01[1]
                        mue01[1] = 2 * mue01[1]
                    else:
                        fnull_n[3] = fnull_n[1]
                        mue01[3] = mue01[1]
                        mue01[1] = (mue01[2] + mue01[3]) / 2
                    
                else:
                    if fnull_n[1] * fnull_n[2] < 0 :
                        fnull_n[3] = fnull_n[1]
                        mue01[3] = mue01[1]
                    else:
                        fnull_n[2] = fnull_n[1]
                        mue01[2] = mue01[1]
                    mue01[1] = (mue01[2] + mue01[3]) / 2
                Variable.stbZRNk = mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
                fnull_n[1] = Variable.stboNk - Variable.stbZRNk
            Variable.stbZRMk = mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
            fnull_m[1] = Variable.stboMk - Variable.stbZRMk
            while abs(fnull_m[1]) > stbkepse5 and it_m < stbkitmax:
                it_m = it_m + 1    
                if it_m == 2 :
                    fnull_m[2] = fnull_m[1]
                    eps2[2] = eps2[1]
                    eps2[1] = 0
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
                it_n = 1
                it_ult = 1
                mue01[1] = Variable.stbZmue0[1]  
                Variable.stbZRNk = mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
                fnull_n[1] = Variable.stboNk - Variable.stbZRNk
                while abs(fnull_n[1]) > stbkepse5 and it_ult < stbkitmax:
                    it_n = it_n + 1
                    it_ult = it_ult + 1
                    if it_n == 2 :
                        fnull_n[2] = fnull_n[1]
                        mue01[2] = mue01[1]
                        mue01[1] = 2 * mue01[1]
                    elif it_n == 3 :
                        if fnull_n[1] * fnull_n[2] > 0 :
                            it_n = 2
                            fnull_n[2] = fnull_n[1]
                            mue01[2] = mue01[1]
                            mue01[1] = 2 * mue01[1]
                        else:
                            fnull_n[3] = fnull_n[1]
                            mue01[3] = mue01[1]
                            mue01[1] = (mue01[2] + mue01[3]) / 2
                        
                    else:
                        if fnull_n[1] * fnull_n[2] < 0 :
                            fnull_n[3] = fnull_n[1]
                            mue01[3] = mue01[1]
                        else:
                            fnull_n[2] = fnull_n[1]
                            mue01[2] = mue01[1]
                        mue01[1] = (mue01[2] + mue01[3]) / 2
                    Variable.stbZRNk = mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
                    fnull_n[1] = Variable.stboNk - Variable.stbZRNk
                Variable.stbZRMk = mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
                fnull_m[1] = Variable.stboMk - Variable.stbZRMk
            if it_ult == stbkitmax :
                Variable.stbZbFehler = True
            else:
                Variable.stbZmue0[1] = mue01[1]
                Variable.stbZmue0[2] = mue02
    elif Variable.stbZsymm == True :
        it_n = 1
        it_ult = 1
        mue01[1] = Variable.stbZmue0[1] 
        mue02 = mue01[1]
        it_m = 1
        eps2[1] = eps0
        Variable.stbZepsck[1] = eps2[1]
        Sepsc2s2()
        Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
        fnull_m[1] = Variable.stboMk - Variable.stbZRMk
        while abs(fnull_m[1]) > stbkepse7 and it_m < stbkitmax:
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
            Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
            fnull_m[1] = Variable.stboMk - Variable.stbZRMk
        Variable.stbZRNk = stbfalpha() * stbfRnbU() + mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
        fnull_n[1] = Variable.stboNk - Variable.stbZRNk
        while abs(fnull_n[1]) > stbkepse5 and it_ult < stbkitmax:
            it_n = it_n + 1
            it_ult = it_ult + 1
            if it_n == 2 :
                if it_m == stbkitmax :    
                    it_n = 1
                else:
                    fnull_n[2] = fnull_n[1]
                    mue01[2] = mue01[1]
                
                mue01[1] = 2 * mue01[1]
            elif it_n == 3 :
                if fnull_n[1] * fnull_n[2] > 0 :
                    it_n = 2
                    fnull_n[2] = fnull_n[1]
                    mue01[2] = mue01[1]
                    mue01[1] = 2 * mue01[1]
                else:
                    fnull_n[3] = fnull_n[1]
                    mue01[3] = mue01[1]
                    mue01[1] = (mue01[2] + mue01[3]) / 2
                
            else:
                if fnull_n[1] * fnull_n[2] < 0 :
                    fnull_n[3] = fnull_n[1]
                    mue01[3] = mue01[1]
                else:
                    fnull_n[2] = fnull_n[1]
                    mue01[2] = mue01[1]
                
                mue01[1] = (mue01[2] + mue01[3]) / 2
            
            mue02 = mue01[1]
            it_m = 1
            eps2[1] = eps0
            Variable.stbZepsck[1] = eps2[1]
            Sepsc2s2()
            Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
            fnull_m[1] = Variable.stboMk - Variable.stbZRMk
            while abs(fnull_m[1]) > stbkepse7 and it_m < stbkitmax:
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
                Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
                fnull_m[1] = Variable.stboMk - Variable.stbZRMk
            Variable.stbZRNk = stbfalpha() * stbfRnbU() + mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
            fnull_n[1] = Variable.stboNk - Variable.stbZRNk
        
        if it_ult == stbkitmax :
            Variable.stbZbFehler = True
        else:
            Variable.stbZmue0[1] = mue01[1]
            Variable.stbZmue0[2] = mue02
    mue02 = Variable.stbZmue0[2]
    it_n = 1
    it_ult = 1
    mue01[1] = Variable.stbZmue0[1]
    it_m = 1
    eps2[1] = eps0
    Variable.stbZepsck[1] = eps2[1]
    Sepsc2s2()
    Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
    fnull_m[1] = Variable.stboMk - Variable.stbZRMk
    while abs(fnull_m[1]) > stbkepse7 and it_m < stbkitmax: 
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
        Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
        fnull_m[1] = Variable.stboMk - Variable.stbZRMk
    Variable.stbZRNk = stbfalpha() * stbfRnbU() + mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
    fnull_n[1] = Variable.stboNk - Variable.stbZRNk
    while abs(fnull_n[1]) > stbkepse5 and it_ult < stbkitmax:
        it_n = it_n + 1
        it_ult = it_ult + 1
        if it_n == 2 :
            if it_m == stbkitmax :   
                it_n = 1
            else:
                fnull_n[2] = fnull_n[1]
                mue01[2] = mue01[1]
            
            mue01[1] = 2 * mue01[1]
        elif it_n == 3 :
            if fnull_n[1] * fnull_n[2] > 0 :
                it_n = 2
                fnull_n[2] = fnull_n[1]
                mue01[2] = mue01[1]
                mue01[1] = 2 * mue01[1]
            else:
                fnull_n[3] = fnull_n[1]
                mue01[3] = mue01[1]
                mue01[1] = (mue01[2] + mue01[3]) / 2
            
        else:
            if fnull_n[1] * fnull_n[2] < 0 :
                fnull_n[3] = fnull_n[1]
                mue01[3] = mue01[1]
            else:
                fnull_n[2] = fnull_n[1]
                mue01[2] = mue01[1]
            
            mue01[1] = (mue01[2] + mue01[3]) / 2
        
        it_m = 1
        eps2[1] = eps0
        Variable.stbZepsck[1] = eps2[1]
        Sepsc2s2()
        Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
        fnull_m[1] = Variable.stboMk - Variable.stbZRMk
        while abs(fnull_m[1]) > stbkepse7 and it_m < stbkitmax: 
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
            Variable.stbZRMk = stbfalpha() * stbfRmbU() + mue01[1] * stbfRmeU1() + mue02 * stbfRmeU2()
            fnull_m[1] = Variable.stboMk - Variable.stbZRMk
        Variable.stbZRNk = stbfalpha() * stbfRnbU() + mue01[1] * stbfRneU1() + mue02 * stbfRneU2()
        fnull_n[1] = Variable.stboNk - Variable.stbZRNk

    if it_ult == stbkitmax :
        Variable.stbZbFehler = True
    else:
        Variable.stbZmue0[1] = mue01[1]
        Variable.stbZmue0[2] = mue02
    # print("SIGVOR_r")

def BruchC1S1():
    Nui = [0,0,0]
    Mui = [0,0,0]

    if Variable.stboNorm == 0:
        SgamC1()
    elif Variable.stboNorm > 0:
        if Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2] > Variable.stbZmue0[0] + Variable.stbZmue0[1] + Variable.stbZmue0[2] + stbkepse7:
            Variable.stbZgamC[1] = Variable.stbogamC[1]+(Variable.stbogamC[0] - Variable.stbogamC[1]) * (1 - (Variable.stbZmue0[0] + Variable.stbZmue0[1] + Variable.stbZmue0[2]) / (Variable.stbomue0Druc[0] + Variable.stbomue0Druc[1] + Variable.stbomue0Druc[2]))
        else:
            Variable.stbZgamC[1] = Variable.stbogamC[1]
        
        Variable.stbZgamS[1] = Variable.stbogamS[1]
    

    Bruch_R()
    
    Nui[0] = stbfRnbU()
    Mui[0] = stbfRmbU()
    Variable.stbZNucs[0] = Nui[0] / Variable.stbZgamC[1]
    if Nui[0] < -stbkepse7:
        Variable.stbZzi[0] = Mui[0] / Nui[0] * Variable.stboD
    else:
        Variable.stbZzi[0] = 0
    
    Variable.stbZNucs[1] = 0
    Variable.stbZNucs[2] = 0
    Variable.stbZzi[1] = 0
    Variable.stbZzi[2] = 0
    Nui[1] = stbfRneU1()
    Mui[1] = stbfRmeU1()
    Nui[2] = stbfRneU2()
    Mui[2] = stbfRmeU2()
    if Variable.stbZmue0[1] > stbkepse7:
        if Nui[1] > stbkepse7:
            Variable.stbZNucs[1] = Variable.stbZNucs[1] + Variable.stbZmue0[1] * Nui[1] / Variable.stbZgamS[1]
            Variable.stbZzi[1] = (Variable.stbZzi[1] * Variable.stbZNucs[1] + Mui[1] / Nui[1] * Variable.stboD * Variable.stbZmue0[1] * Nui[1] / Variable.stbZgamS[1]) / Variable.stbZNucs[1]
        elif Nui[1] < -stbkepse7:
            Variable.stbZNucs[2] = Variable.stbZNucs[2] + Variable.stbZmue0[1] * Nui[1] / Variable.stbZgamS[1]
            Variable.stbZzi[2] = (Variable.stbZzi[2] * Variable.stbZNucs[2] + Mui[1] / Nui[1] * Variable.stboD * Variable.stbZmue0[1] * Nui[1] / Variable.stbZgamS[1]) / Variable.stbZNucs[2]
        
    
    if Variable.stbZmue0[2] > stbkepse7:
        if Nui[2] < -stbkepse7:
            Variable.stbZNucs[2] = Variable.stbZNucs[2] + Variable.stbZmue0[2] * Nui[2] / Variable.stbZgamS[1]
            Variable.stbZzi[2] = (Variable.stbZzi[2] * Variable.stbZNucs[2] + Mui[2] / Nui[2] * Variable.stboD * Variable.stbZmue0[2] * Nui[2] / Variable.stbZgamS[1]) / Variable.stbZNucs[2]
        elif Nui[2] > stbkepse7:
            Variable.stbZNucs[1] = Variable.stbZNucs[1] + Variable.stbZmue0[2] * Nui[2] / Variable.stbZgamS[1]
            Variable.stbZzi[1] = (Variable.stbZzi[1] * Variable.stbZNucs[1] + Mui[2] / Nui[2] * Variable.stboD * Variable.stbZmue0[2] * Nui[2] / Variable.stbZgamS[1]) / Variable.stbZNucs[1]
        
    if Variable.stbZNucs[0] < -stbkepse7 and Variable.stbZNucs[1] > stbkepse7:
        zD = (Variable.stbZzi[0] * Variable.stbZNucs[0] + Variable.stbZzi[2] * Variable.stbZNucs[2]) / (Variable.stbZNucs[0] + Variable.stbZNucs[2])
        Variable.stbZNucs[3] = min(abs(Variable.stbZNucs[0] + Variable.stbZNucs[2]), Variable.stbZNucs[1])
        Variable.stbZzi[3] = Variable.stbZzi[1] - zD
    else:
        Variable.stbZNucs[3] = 0
        Variable.stbZzi[3] = 0
    #print(BruchC1S1)


def stbfAcc():
    if Variable.stbZepscd[2] < stbkepse7:
        stbfAcc = Variable.stboRB * Variable.stboD
        
    elif Variable.stbZepscd[1] > -stbkepse7:
        stbfAcc = 0
    else:
        xgr = Variable.stboD * Variable.stbZepscd[1] / (Variable.stbZepscd[1] - Variable.stbZepscd[2])
        stbfAcc = Variable.stboRB * xgr
    return stbfAcc

def stbfzi():
    mue1 = 0
    mue2 = 0
    SRechenWerteZ(1)
    mue1 = Variable.stbZmue0[1] 
    mue2 = Variable.stbZmue0[2] 
    
    stbfzi = Variable.stbZzi[3]
    if Variable.stbZepscd[1] > -stbkepse5 and mue1 > stbkepse7 and mue2 > stbkepse7:
        stbfzi = Variable.stboHQ - Variable.stbZ_H[1] - Variable.stbZ_H[2]
    else:
        stbfzi = max(stbfzi, 0.9 * (Variable.stboHQ - Variable.stbZ_H[1]))
        stbfzi = min(stbfzi, max(Variable.stboHQ - 2 * Variable.stbZ_H[2], Variable.stboHQ - Variable.stbZ_H[2] - 0.03))
    return stbfzi


def QuerBemessN0():
    f_ctd = stbffctm() / Variable.stbZgamC[1]                                                         
    Nd1 = Variable.stboNd * Variable.stboRB * Variable.stboD * Variable.stbofck
    Qd = Variable.stboQd * Variable.stboRB * Variable.stboD * Variable.stbofck
    vormue1 = Variable.stbZmue0[1]
    Rctd = f_ctd * Variable.stboRB * Variable.stboD
    

    if vormue1 < stbkepse7:

        Variable.stbZtau0 = Qd / stbfAcc()                                      
        sig_x = Nd1 / stbfAcc()                                          
        Variable.stbZtau0 = sig_x / 2 + math.sqrt((sig_x / 2) ** 2 + Variable.stbZtau0 ** 2)   

        if Variable.stbZtau0 <= Variable.stbotau012:
            stbZerfas = 0
        else:
            stbZerfas = -1
        

    else:

        if Variable.stbZepscd[2] < stbkepse5:
            Variable.stbZtau0 = Qd / stbfAcc()
            sig_x = Nd1 / stbfAcc()
            Variable.stbZtau0 = sig_x / 2 + math.sqrt((sig_x / 2) ** 2 + Variable.stbZtau0 ** 2)
        else:
            Variable.stbZtau0 = Qd / Variable.stboBQ / stbfzi()
        

        if Variable.stbZtau0 <= Variable.stbotau012:
            if Nd1 > Rctd:
                tau = Variable.stbZtau0
            else:
                tau = 0.4 * Variable.stbZtau0
                if Nd1 > 0:
                    tau = tau + (Variable.stbZtau0 - tau) * Nd1 / Rctd
                
            
        elif Variable.stbZtau0 <= Variable.stbotau02:
            if Nd1 > Rctd:
                tau = Variable.stbZtau0
            else:
                tau = max(Variable.stbZtau0 ** 2 / Variable.stbotau02, 0.4 * Variable.stbZtau0)
                if Nd1 > 0:
                    tau = tau + (Variable.stbZtau0 - tau) * Nd1 / Rctd
                
            
        elif Variable.stbZtau0 <= Variable.stbotau03:
            if Variable.stbZepscd[1] > -stbkepse5:
                tau = -1
            else:
                tau = Variable.stbZtau0
            
        else:
            tau = -1
        
        if tau <= -0.5:
            stbZerfas = -1
        else:
            stbZerfas = tau * Variable.stboBQ / (Variable.stbofyk / Variable.stbogamS[1]) * 10000
    #print(QuerBemessN0)


def QuerBemessN123():
    zi = 0
    SRechenWerteZ(1)
    f_cd = Variable.stbofck / Variable.stbZgamC[1]                                                                
    f_ctd = stbffctm() / Variable.stbZgamC[1]                                                            
    f_yd = Variable.stbofyk / Variable.stbogamS[1]                                                                
    Nd1 = Variable.stboNd * Variable.stboRB * Variable.stboD * Variable.stbofck
    Qd = Variable.stboQd * Variable.stboRB * Variable.stboD * Variable.stbofck
    vormue1 = Variable.stbZmue0[1]
    Rctd = f_ctd * Variable.stboRB * Variable.stboD

    if vormue1 < stbkepse7:
        if Variable.stboNorm == 1:
            sigcp = -Nd1 / Variable.stboBQ / Variable.stboHQ                                                      
        elif Variable.stboNorm == 2 or Variable.stboNorm == 3:
            sigcp = -Nd1 / stbfAcc()                                                             
                                                                                         
        if Variable.stboNorm == 1:
            Variable.stbZtaucp = 1.5 * Qd / Variable.stboBQ / Variable.stboHQ                                             
            Variable.stbZfcvd = math.sqrt(f_ctd ** 2 + sigcp * f_ctd)                                         
        elif Variable.stboNorm == 2 or Variable.stboNorm == 3:
            Variable.stbZtaucp = 1.5 * Qd / stbfAcc()                                                   
            sig_clim = f_cd - 2 * math.sqrt(f_ctd * (f_ctd + f_cd))                               
            if sigcp <= sig_clim:                                                         
                Variable.stbZfcvd = math.sqrt(f_ctd ** 2 + sigcp * f_ctd)
            else:
                Variable.stbZfcvd = math.sqrt(max(f_ctd ** 2 + sigcp * f_ctd - (sigcp - sig_clim) ** 2 / 4, 0))
            
            Variable.stbZVRdc = stbfAcc() * Variable.stbZfcvd / 1.5
    
        Variable.stbZminas = 0
        if Qd <= Variable.stbZVRdc + stbkepse5:
            Variable.stbZerfas = 0
        else:
            Variable.stbZerfas = -1
    else:
        zi = stbfzi()
        DQ = Variable.stboHQ - Variable.stbZ_H[1]                                          
        sigcp = -Nd1 / Variable.stboBQ / Variable.stboHQ                                           
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
        if Variable.stboNorm == 1 or Variable.stboNorm == 3:
            nue1 = 0.75                                                                        
        elif Variable.stboNorm == 2:
            nue1 = 0.6                                                                   
        
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
        if Variable.stboNorm == 1 or Variable.stboNorm == 3:                                                  
            Variable.stbZminas = 0.16 * stbffctm() / Variable.stbofyk * Variable.stboBQ * 10000                           
        elif Variable.stboNorm == 2:
            Variable.stbZminas = 0.08 * math.sqrt(Variable.stbofck) / Variable.stbofyk * Variable.stboBQ * 10000                        
        if Qd <= Variable.stbZVRdc + stbkepse5:
            Variable.stbZerfas = Variable.stbZminas
        elif Qd <= Variable.stbZVRdmax + stbkepse5:
            Variable.stbZerfas = Qd / f_yd / zi / Variable.stbZcottheta * 10000
            if Variable.stbZerfas < Variable.stbZminas:
                Variable.stbZerfas = Variable.stbZminas
                if Variable.stbZcottheta > 1 + stbkepse5 and Variable.stbomaxcottheta <= stbkepse3:
                    Variable.stbZcottheta = max(Qd / f_yd / zi / Variable.stbZerfas * 10000, 1)           
                    Variable.stbZVRdmax = Variable.stboBQ * zi * nue1 * f_cd / (Variable.stbZcottheta + 1 / Variable.stbZcottheta) 
        else:
            Variable.stbZerfas = -1
    #print( QuerBemessN123)


if __name__ == "__main__":
    for i in range(11,29):
        print(StB_R_MN(3,1.5,1.15,26616.89535,0,19716.2191,0,1500,2500,100,100,False,5,5,25,0.85,0.002,0.0035,2,0.15,"0.15 0",500,520,200000,0.025,200,1,i))
    for i in range(11,24):
        print(i,StB_R_Q(3,1.5,1.15,26616.89535,0,1229,1500,2500,100,100,5,5,25,0.85,0.002,0.0035,2,0.15,"0.15 0",500,520,200000,0.025,0,0,0,i))
    As1 = StB_R_MN(3,1.5,1.15,4.25388051219,0.0,3.15102260162,0,800.0,2800.0,100.0,100.0,False,5,5,35.0,0.85,0.002,0.0035,2.0,0.15,"0.15 0",500.0,520.0,200000.0,0.025,240.0,1,17)
    As2 = StB_R_MN(3,1.5,1.15,4.25388051219,0.0,3.15102260162,0,800.0,2800.0,100.0,100.0,False,5,5,35.0,0.85,0.002,0.0035,2.0,0.15,"0.15 0",500.0,520.0,200000.0,0.025,240.0,1,18)
    asl = StB_R_Q(3,1.5,1.15,4.25388051219,0.0,36.8160369762,800.0,2800.0,100.0,100.0,As1,As2,35.0,0.85,0.002,0.0035,2.0,0.15,"0.15 0",500.0,520.0,200000.0,0.025,0,0,0,19)
    print(As1,As2,asl)
    t = StB_R_MN(3,1.5,1.15,-377.603311774,0,-188.801655887,0,500.0,2500.0,100.0,100.0,False,5,5,25.0,0.85,0.002,0.0035,2.0,0.15,"0.15 0",500.0,520.0,200000.0,0.025,300.0,2,18)
    k = StB_R_MN(3,1.5,1.15,14601.3484044,0,10815.8136329,0,1800,2500,100,100,False,5,5,30,0.85,0.002,0.0035,2,0.15,"0.15 0",500,520,200000,0.025,300,1,17)
    print(t,k)
    print(StB_R_Q(3,1.5,1.15,8841.43665144,0,-5361.23283345,1800.0,2500.0,100.0,100.0,0,0,30.0,0.85,0.002,0.0035,2.0,0.15,"0.15 0",500.0,520.0,200000.0,0.025,0,0,0,19))
    StB_R_MN(3,1.5,1.15,-377.603311774,0,-188.801655887,0,500.0,2500.0,100.0,100.0,False,5,5,25.0,0.85,0.002,0.0035,2.0,0.15,"0.15 0",500.0,520.0,200000.0,0.025,300.0,2,17)