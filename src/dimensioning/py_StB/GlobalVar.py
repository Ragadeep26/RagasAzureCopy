# 
# Variable mit konstantem Wert

# stboNachweis:  1 = Biegung mit Normalkraft
#                2 = Querkraft
# stboNachweis  
# stboQuer:      1 = Kreisquerschnitt
#                2 = Kreisquerschnitt mit sektionaler Bewehrung
#                3 = Rechteckquerschnitt
# stboQuer  
# stboNorm:      0 = DIN 1045:1988
#                1 = DIN 1045:2008
#                2 = EN 1992-1-1:2004  (Eurocode 2)
#                3 = DIN EN 1992-1-1:2004 + AC:2010 + NA:2011
# stboNorm  
# Geometrische Grundwerte
# stboD               Dicke des Betonquerschnittes (Kreis oder Rechteck) [m]
# stboRB              Breite des Recheckquerschnittes                    [m]
# stboKR              Radius des Kreisquerschnittes                      [m]
# stboH(2)            Randabstand der Bewehrung                          [m]
#                                     Kreis:     stboH(2) = stboH(1)
#                                     Rechteck:  stboH(2) = Randabstand der oberen Bewehrung (in der Regel Druck)
#                                                stboH(1) = Randabstand der unteren Bewehrung (in der Regel Zug)
#                                                Im Funktionsaufruf ist der Druckrand geometrisch "oben" festegelegt. Bei einem negativen Moment (stboVMd, stboVMk < 0#) ist der
#                                                funktionelle Druckrand jedoch "unten". Druck- und Zugrand können sich also für Bruchschnittgrößen und Gebrauchsschnittgrößen unterscheiden.
#                                                Deshalb wird beim Aufruf von Funktionen, in denen der Randabstand eine Rolle spielt, dieser Parameter mit dem Aufruf übergeben.
#                                     In den Rechenroutinen werden deshalb die zustandsabhängigen Variablen stbZ_H(1) für Zug und stbZ_H(2) für Druck verwendet.
# stboRe              Radius des Bewehrungskreises                       [m]
# stbodelt2           Halber Öffnungswinkel des Tragbereiches            [Rad]
#                                     Schwerpunkt des Tragbereichsbogens: S = stboRe * sin(stbodelt2) / stbodelt2 bzw. S = stboRe für stbodelt2 < stbkepse5
# stbobHkrit          Für Querschnitte mit ungleichem Randabstand der Bewehrung (stbobHkrit = True, nur bei Rechteckquerschnitt möglich) müssen bei bestimmten
#                                     Iterationen in den Subroutinen SgamC1 und SRissB, konservative Ansätze getroffen werden, weil ansonsten bei bestimmten Schnittgrößenkombinationen
#                                     die Konvergenz nicht gesichert ist. Diese Iterationen werden durch den Wert von stbobHkrit beeinflusst.
#                                      For cross sections with uneven edge spacing of the reinforcement (stbobHkrit = True, only possible with a rectangular cross section) certain
#                                     Iterations in the subroutines SgamC1 and SRissB, conservative approaches are taken because otherwise with certain combinations of internal forces
#                                     the convergence is not sured. These iterations are affected by the value of stbobHkrit.
# stboeBewk  Double
# Beton
# stbofck             Beton-Druckfestigkeit (Würfelfestigkeit für Norm = 0, Zylinderfestigkeit für Norm > 0) [MN/m^2]
# stboalpha           Abminderungsbeiwert für die Beton-Druckfestigkeit  [1]
# stboepscy           Beginn der pltischen Betondehnung (Ende des Parabelzweiges)  [1]
# stboepscu           Bruchdehnung des Betons (Ende der pltischen Stauchung)       [1]
# stbon2              Parabelexponent des Betons                         [1]
# Bewehrung
# stbofyk             Streckgrenze der Bewehrung                         [MN/m^2]
# stboftk             Zugfestigkeit des Bewehrung                        [MN/m^2]
# stboepssy           Dehnung an der Streckgrenze                        [1]
# stboepssu           Bruchdehnung                                       [1]
# Bezogene bzw. reduzierte Schnittgrößen
#   Kreis:       stboNd = Nd / 1000# / stboKR ^ 2 / stbofck
#                stboMd = Abs(Md) / 1000# / stboKR ^ 3 / stbofck
#                stboQd = Abs(Qd) / 1000# / stboKR ^ 2 / stbofck
#   Rechteck:    stboNd = Nd / 1000# / stboRB / stboD / stbofck
#                stboMd = Abs(Md) / 1000# / stboRB / stboD ^ 2 / stbofck
#                stboQd = Abs(Qd) / 1000# / stboRB / stboD / stbofck
# stboNd              Normalkraft, Bemessungswert                        [1]
# stboMd              Biegemoment, Bemessungswert                        [1]
# stboQd              Querkraft, Bemessungswert                          [1]
# stboNk              Normalkraft, charakteristischer Wert               [1]
# stboMk              Biegemoment, charakteristischer Wert               [1]
# Ltausmitte     e = stboMx / stboNx maximal = 1# für kleine Werte von stboNx
# stboeNd             Ausmitte, Bemessung bezogen auf stboKR bzw. stboD  [1]
# stboeNk             Ausmitte, charakt. bezogen auf stboKR bzw. stboD   [1]
# Schalter für Vorzeichen des Biegemomentes
#   0:   positives Vorzeichen oder Nullstab
#   1:   negatives Vorzeichen
# stboVMd                Vorzeichen für d Bemessungsmoment
# stboVMk                Vorzeichen für d charakteristische Moment
# Nullstab
#   Wahr, wenn   Abs(stboNd) und stboMd < stbkepse5   bzw.   Abs(stboNk) und stboMk < stbkepse5
# stboNullSd          Nullstab für Bemessungsschnittgrößen
# stboNullSk          Nullstab für charakteristische Schnittgrößen
# Beltungsart (ermittelt mit Bemessungsschnittgrößen)
# stbobDruc(1) = True:   Es gibt eine Druckkraft
# stbobDruc(2) = True:   Die Resultierende aus Druckkraft und Moment liegt innerhalb der Querschnittsfläche
# stbobDruc(3) = True:   Die Ausmitte der Resultierenden aus Druckkraft und Moment e < 0.4 * stboD für Rechteckquerschnitte
#                        bzw. e < 0.3803 * stboD für Kreisquerschnitte (gleicher Dehnungszustand wie beim Rechteckquerschnitt)
# stbobDruc(3)  
# Hilfsvariable für die Ermittlung / Optimierung der statisch erforderlichen Bewehrungsmenge (Bruchzustand)
# stbodehnkrit(0 To 3)    Besondere Dehnungszustände als Startwerte für die Iteration
# stbomue0Dehn(3, 3)      Besondere Bewehrungsgehalte als Startwerte für den Optimierungsalgorithmus
# Mechanischer Bewehrungsgehalt:
# Kreisquerschnitt:      mue0 =  / stbkPi / stboKR ^ 2 * stboftk / stbofck
# Rechteckquerschnitt:   mue0 =  / stboD / stboRB * stboftk / stbofck
# Index 0:   Kreisringbewehrung
# Index 1:   Zugbewehrung bei Rechteckquerschnitt und sektionaler Bewehrung
# Index 2:   Druckbewehrung bei Rechteckquerschnitt und sektionaler Bewehrung
# stbovormue0(0 To 2)     vorgegebener Bewehrungsgehalt
# stbomue0Riss(0 To 2)    Mindestbewehrung für d Rissmoment
# Grundwerte der Sicherheitsbeiwerte und Hilfsgrößen: Der Teilsicherheitsbeiwert für Beton stbogamC beinhaltet den Abminderungswert stboalpha
# stbogamC(-1 To 0)       Grundwerte des Teilsicherheitsbeiwertes für Beton (für Druck | Zug)
# stbogamS(-1 To 0)       Grundwerte des Teilsicherheitsbeiwertes für die Bewehrung (für Druck | Zug)
# stboepsSmin(2)          für stboNorm = 0: Dehngrenzen für erhöhten Sicherheitsbeiwert bei druckbeanspruchten Querschnitten
# stbomue0Druc(0 To 2)    für stboNorm > 0: Mindestbewehrung für druckbeltete Querschnitte, erhöhte Sicherheitsbeiwerte falls diese Bewehrung unterschritten wird
# Symmetrische Bewehrung wird vorgegeben (nur für stboQuer = 2 und stboQuer = 3)
# stbosymmue0  
# Rissbreitenbegrenzung: maximale Stahlspannung im Gebrauchszustand, stboRissP1 < 1# --> keine Rissbreitenbegrenzung
# stboRissP1              [MPa]
# Mindestbewehrung vorgegeben oder erforderlich wegen zu großer klaffender Fuge (stbZerfmue0 >= stbomue0Riss)
# Minimum reinforcement specified or required due to gaping gap (stbZerfmue0> = stbomue0Riss)
# stbobminBew  
# Schalter für Rückgabewert
# stboii  




# Variable mit veränderlichem Wert (Zustandsvariable)

# stbZgamC(1) und stbZgamS(1) sind die Teilsicherheitsbeiwerte für Beton und Bewehrung in Abhängigkeit vom Dehnungszustand
# stbZgamC (1) and stbZgamS (1) are the partial safety factors for concrete and reinforcement depending on the state of expansion
# stbZgamC(3)             Die Werte mit Index 2 und 3 sind Hilfswerte, die bei der iterativen ErmittlungThe values ​​with index 2 and 3 are auxiliary values ​​that are used in the iterative determination
# stbZgamS(3)             von stbZgamC(1) und stbZgamS(1) verwendet werden.
# stbZnue0                vorhandene Sicherheit für den unbewehrten Querschnitt

# Beton- und Stahldehnungen:
# Der Dehnungszustand muss für die Stahlbetonbemessung iterativ ermittelt werden
# stbZepscd(2)            Betondehnungen, Bruchzustand                       [1]
# stbZepssd(2)            Stahldehnungen, Bruchzustand                       [1]
# stbZepsck(2)            Betondehnungen, Gebrauchszustand                   [1]
# stbZepssk(2)            Stahldehnungen, Gebrauchszustand                   [1]

# Dimensionslose bezogene bzw. reduzierte innere Widerstände:
# Neben den Dehnungen sind d die zentralen Werte, die für die Stahlbetonbemesseungen iterativ ermittelt werden
# stbZRNd                 Normalkraft, Bemessungswert                        [1]
# stbZRMd                 Biegemoment, Bemessungswert                        [1]
# stbZRNk                 Normalkraft, charakteristischer Wert               [1]
# stbZRMk                 Biegemoment, charakteristischer Wert               [1]
# Mechanischer Bewehrungsgehalt:
# Kreisquerschnitt:      mue0 =  / stbkPi / stboKR ^ 2 * stboftk / stbofck
# Rechteckquerschnitt:   mue0 =  / stboD / stboRB * stboftk / stbofck
# Index 0:   Kreisringbewehrung
# Index 1:   Zugbewehrung bei Rechteckquerschnitt und sektionaler Bewehrung
# Index 2:   Druckbewehrung bei Rechteckquerschnitt und sektionaler Bewehrung
# stbZerfmue0(0 To 2)     erforderlicher Bewehrungsgehalt (ggf. einschließlich Mindestbewehrung stbomue0Riss)
# stbZmue0(0 To 2)        ermittelter Bewehrungsgehalt

# Symmetrische Bewehrung wird angesetzt (nur für stboQuer = 2 und stboQuer = 3)
# stbZsymm  

# Querkraftbemessung
# stboHQ                  Querschnittsdicke  Kreis --> flächengleiches       [m]
# stboBQ                  Querschnittsbreite           Quadrat               [m]
# stbZNucs(0 To 3)        bezogene bzw. reduzierte innere Schnittgrößen      {1]
#                                         0: Betondruckkraft
#                                         1: Stahlzugkraft
#                                         2: Stahldruckkraft
#                                         3: Kraft (Betrag) des resultierenden inneren Kräftepaars
# stbZzi(0 To 3)          zu den inneren Kräften zugehörige Hebelarme        [m]
# stbZerf               erforderliche Querkraftbewehrung                   [cm^2/m]
# für stboNorm = 0
# stbZtau0                vorhandene Schubbeanspruchung                      [MN/m^2]
# stbotau012              untere Grenze der Schubbeanspruchung               [MN/m^2]
# stbotau02               mittlere Grenze der Schubbeanspruchung             [MN/m^2]
# stbotau03               obere Grenze der Schubbeanspruchung                [MN/m^2]
# stbotau1                Grundwert der Verbundspannung für Bereich I        [MN/m^2]
# stbotau2                Grundwert der Verbundspannung für Bereich II       [MN/m^2]
# für stboNorm > 0
# stbZmin               Mindestschubbewehrung                              [cm^2/m]
# stbZVRdc                Querkraftwiderstand ohne Schubbewehrung            [MN]
# bewehrter Querschnitt
# stbZVRdmax              maximaler Querkraftwiderstand                      [MN]
# stbZcottheta            Neigung der Druckstreben                           [1]
# stbomaxcottheta         Neigung der Druckstreben (optionale Vorgabe)       [1]
# unbewehrter Querschnitt
# stbZtaucp               maximale Schubspannung im Querschnitt              [MPa]
# stbZfcvd                Bemesssungsfestigkeit für kombinierte Druck-/Schubbeanspruchung    [MPa]

# Zustandsflag
# stbZiZ = 1:    Bruchzustand
# stbZiZ = 2:    Gebrauchszustand
# stbZiZ  

# Rechenwerte, den je nach Wert von stbZiZ unterschiedliche Eingabegrößen oder Zustandsgrößen zugewiesen werden
# Geometrische Grundwerte
# stbZ_H(2)               Randabstand der Bewehrung                          [m]
# Beton- und Stahldehnungen:
# stbZeps_c(2)            Betondehnungen                                     [1]
# stbZeps_s(2)            Stahldehnungen                                     [1]

# Fehlermelder wird zunächst auf falsch gesetzt und wird wahr, wenn in einer Iterationsschleife stbkitmax erreicht wird
# stbZbFehler  

time = [0,0,0,0,0]
Atime = 0
erfmuetime = []
gebrauchtime = []
sigvortime = []
stbkbKlaffPruef= True
stboNachweis = 1
stboQuer = 0
stboNorm = 0
stboD = 0             
stboRB = 0          
stboKR  = 0       
stboH  = [0,0,0]     
stboRe = 0          
stbodelt2 = 0      
stbobHkrit = True       
stboeBewk= 0
stbofck   = 0         
stboalpha = 0       
stboepscy  = 0      
stboepscu   = 0       
stbon2   = 0         
stbofyk= 0          
stboftk = 0          
stboepssy = 0       
stboepssu  = 0       
stboNd  = 0           
stboMd= 0            
stboQd  = 0          
stboNk = 0         
stboMk = 0          
stboeNd = 0           
stboeNk = 0         
stboVMd = 0           
stboVMk  = 0           
stboNullSd = 0    
stboNullSk = 0     
Nd1= 0
stbobDruc = [None,False,False,False]
stbodehnkrit = [0,0,0,0]   
stbomue0Dehn = [[0,0,0,0],[0,0,0,0], [0,0,0,0] ,[0,0,0,0]]   
stbovormue0 = [0,0,0]    
stbomue0Riss = [0,0,0]   
stbogamC = [0,0]       
stbogamS= [0,0]       
stboepsSmin = [0,0,0]       
stbomue0Druc= [0,0,0]    
stbosymmue0 = 0
stboRissP1  = 0        

stbobminBew = False
stboii= 0
stbZgamC = [0,0,0,0]          
stbZgamS= [0,0,0,0]          
stbZnue0  = 0         

stbZepscd= [0,0,0]            
stbZepssd= [0,0,0]          
stbZepsck= [0,0,0]         
stbZepssk= [0,0,0]   
stbZRNd  = 0            
stbZRMd  = 0             
stbZRNk  =0          
stbZRMk  =0            
stbZerfmue0= [0,0,0]    
stbZmue0= [0,0,0]      

stbZsymm = 0
stboHQ  = 0          
stboBQ  = 0              
stbZNucs= [0,0,0,0]      
stbZzi= [0,0,0,0]      
stbZerf= 0           
stbZtau0    =0        
stbotau012 =0           
stbotau02  =0         
stbotau03   =0           
stbotau1    =0          
stbotau2      =0         
stbZmin     = 0          
stbZVRdc      = 0         
stbZVRdmax  = 0           
stbZcottheta  = 0       
stbomaxcottheta  = 0      
mue_loop = False
stbZtaucp = 0        
stbZfcvd = 0             
stbZiZ = 1
stbZ_H= [0,0,0]            
stbZeps_c= [0,0,0]          
stbZeps_s= [0,0,0]       
stbZbFehler  = False
imag = 0
tracker = []
looptracker = []


stbotau012 = 0
stbotau02 = 0
stbotau03= 0
stbotau1 = 0
stbotau2 = 0