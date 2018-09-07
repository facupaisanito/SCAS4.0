#-----------------------------------------------------------------------
# ScriptInc  for BA
# Version: 1
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------
#

try:
    import sys,os
except:
    print "import sys,os in scriptSys Not found!!"
    sys.exit()
try:
    sys.argv.append('--Param-scriptSys')
    sys.argv.append(sys.argv[1])
    import scriptSys
except:
    print "ERROR file scriptSys Not found!!"
    sys.exit()
try:
    for px in sys.argv:
        if px == '--Param-scriptInc':
            idx = sys.argv.index(px)
            sys.argv.pop(idx) # remove option
            STATION_N = sys.argv[idx]
            sys.argv.pop(idx) # remove value
except:
    print "ERROR Param-scriptInc en scriptInc !!"
    sys.exit()
try:
    for px in sys.argv:
        if px == '-d':
            scriptSys.DEBUG_MODE = True
            try:
                sys.argv.append('--Param-scriptDebug')
                sys.argv.append(sys.argv[1])
                import scriptDebug
            except:
                print "ERROR file scriptDebug Not found!!"
                sys.exit()
except:
    print "ERROR Param-scriptDebug en scriptInc !!"
    sys.exit()

################################################################
##########                  line1                     ##########
################################################################
def get_line(dType, tLapse):
    try:
        n = len(tLapse)
        if len(tLapse)%2 == 1:
            tLapse.pop()
            n = len(tLapse)
        var = scriptSys.get_data(dType, tLapse)
        VAR = sum(var) / float(len(var)) #promedio
        m = []
        m_aux = []
        for x in range(0 , n , 2):
            m_aux.append((var[x]+var[x+1])/2)
        for x in range((n/2)-1):
            m.append((m_aux[x+1]-m_aux[x])/2)
        M = sum(m) / float(len(m)) #promedio
        VAR1 = VAR + M *(n/2)
        if scriptSys.DEBUG_MODE : scriptDebug.plot_line(dType,M,VAR1,tLapse[-1])
        scriptSys.GENERAL['line_m'] = str(M)
        scriptSys.GENERAL['line_m'] = str(VAR1)
        return
    except:
        scriptSys.error_report("get_line()")
################################################################
##########                  measure_z1                ##########
################################################################
#Setup
tTest1  =   20  #tiempo de descarga suave
tTest2  =   140  #tiempo de descarga fuerte
tTest3  =   400  #tiempo de recuperacion
tTest4  =   200 #tiempo de chequeo e incio de sig etapa
tTest5  =   20
tMargin =   3   #margen de tiempo por no ser 10s exactos
# voltageAverage = 3
# currentAverage = 5
# Z1 = 0
# Z2 = 0
tTestA  =   tTest1
tTestB  =   tTest1 + tTest2
tTestC  =   tTest1 + tTest2 + tTest3
tTestD  =   tTest1 + tTest2 + tTest3 + tTest4
#
def measure_z1() :
    try:
        if scriptSys.GENERAL['mode'] != 'Z_MEASURE' : #si es 1 llamado
            scriptSys.GENERAL['mode'] = 'Z_MEASURE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "DISCHARGE,1.8"
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tTestD :
            scriptSys.final_report(0,0)
            return

        if  actual_time >= (tTestC- tMargin)and actual_time <(tTestC + tMargin):

            print "PAUSE"
            return

        if  actual_time >=(tTestB - tMargin)and actual_time <(tTestB + tMargin):
            print "DISCHARGE,1.0"
            return

        if  actual_time >=(tTestA - tMargin)and actual_time <(tTestA + tMargin):
            print "PAUSE"
            return
        print "RUN"
        return
    except:
        scriptSys.error_report("measure_z1()")
################################################################
##########                  measure_z2                ##########
################################################################
#Setup
tTest12  =   30  #tiempo de descarga suave
tTest22  =   60  #tiempo de descarga fuerte
tTest32  =   60  #tiempo de recuperacion
tTest42  =   20  #tiempo de chequeo e incio de sig etapa
tTest52  =   20
# tMargin =   5   #margen de tiempo por no ser 10s exactos
voltageAverage = 3
currentAverage = 5
Z1 = 0
Z2 = 0
tTestA2  =   tTest12
tTestB2  =   tTest12 + tTest22
tTestC2  =   tTest12 + tTest22 + tTest32
tTestD2  =   tTest12 + tTest22 + tTest32 + tTest42
#
def measure_z2() :
    try:
        if scriptSys.GENERAL['mode'] != 'Z_MEASURE2' : #si es llamado por 1
            scriptSys.GENERAL['mode'] = 'Z_MEASURE2'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "DISCHARGE,1.0"
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tTestD2 :
            # deja reposar y chequea q no caiga la tension
            # scriptSys.final_report(0,0)
            # stress_test()
            scriptSys.GENERAL['mode'] = 'CHARGE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "CHARGE,4.2,1.2"
            # scriptTest.charge_state(1)
            return

        if  actual_time >=(tTestC2 - tMargin) \
            and actual_time <(tTestC2 + tMargin):
            # print "DISCHARGE,1.0"  Descarga fuerte
            scriptSys.import_data()
            #delay en el inicio de la descarga
            t = scriptSys.TIME_INIT + tTestB2 + 2
            var = scriptSys.get_data('VOLTAGE', \
                range( t - 5 , t - 5 + voltageAverage))
                #promedio de las mediciones al principio
            V1 = sum(var) / float(len(var))
            var = scriptSys.get_data('VOLTAGE', \
                range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
                #promedio de las mediciones al final del test
            V2 = sum(var) / float(len(var))
            var = scriptSys.get_data('CURRENT',
                range(scriptSys.TIME - currentAverage,scriptSys.TIME))
                #promedio de las mediciones al principio
            I1 = sum(var) / float(len(var))
            Z2 = int( ( (float(V2)-float(V1))/float(I1) ) *1000 )
            scriptSys.EVAL['int_z2'] = str(Z2)
            scriptSys.EVAL['int_z'] =   str(Z2) #str(round(Z1,0))
            # chequear rectas
            print "PAUSE"
            return

        if  actual_time >=(tTestB2 - tMargin) \
            and actual_time <(tTestB2 + tMargin):
            # deja reposar y chequea q no caiga la tension
            # stress_test()
            print "DISCHARGE,1.5"
            return

        if  actual_time >= (tTestA2 - tMargin) \
            and  actual_time < (tTestA2 + tMargin) :
            # print "DISCHARGE,0.2"  Descarga suave
            scriptSys.import_data()
            t = scriptSys.TIME_INIT + 2 #delay en el inicio de la descarga
            var = scriptSys.get_data('VOLTAGE', \
                range( t - 5, t- 5 + voltageAverage))
                #promedio de las mediciones al principio
            V1 = sum(var) / float(len(var))
            var = scriptSys.get_data('VOLTAGE', \
                range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
                #promedio de las mediciones al final del test
            V2 = sum(var) / float(len(var))
            var = scriptSys.get_data('CURRENT', \
                range( scriptSys.TIME - currentAverage,scriptSys.TIME))
                #promedio de las mediciones al principio
            I1 = sum(var) / float(len(var))
            Z1 = int( ( (float(V2)-float(V1))/float(I1) ) *1000 )

            scriptSys.EVAL['int_z1'] =  str(Z1) #str(round(Z1,3))
            # chequear rectas
            print "PAUSE"
            return
        print "RUN"
        return
    except:
        scriptSys.error_report("measure_z2()")
################################################################
##########                  STRESS                    ##########
################################################################

#Setup
tTest1  =   20  #tiempo de descarga suave
tTest2  =   140  #tiempo de descarga fuerte
tTest3  =   400  #tiempo de recuperacion
tTest4  =   200 #tiempo de chequeo e incio de sig etapa
tTest5  =   20
# tTest1  =   20  #tiempo de descarga suave
# tTest2  =   10  #tiempo de descarga fuerte
# tTest3  =   40  #tiempo de recuperacion
# tTest4  =   30 #tiempo de chequeo e incio de sig etapa
# tTest5  =   20
tMargin =   4   #margen de tiempo por no ser 10s exactos
# voltageAverage = 3
# currentAverage = 5
# Z1 = 0
# Z2 = 0
tTestA  =   tTest1
tTestB  =   tTest1 + tTest2
tTestC  =   tTest1 + tTest2 + tTest3
tTestD  =   tTest1 + tTest2 + tTest3 + tTest4
iCharge1 =          '0.5'
vCharge1 =          '4.2'
iDischargeTest1 =   '1.5'
iDischargeTest2 =   '1.0'
tMaxStress =     	4 * 60 * 60 # 4 hr
vMargin =           16
lowVoltageLimit =   3000
maxTimeInitFail =   40          # 10 seg
#
def stress_test() :
    try:
        if scriptSys.GENERAL['mode'] != 'STRESS' : #si es llamado por 1
            scriptSys.GENERAL['mode'] = 'STRESS'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "DISCHARGE,"+ iDischargeTest1
            return
        if  scriptSys.VOLTAGE <= vMargin:
            scriptSys.final_report("maxTimeInitFail",0)
            return
        if scriptSys.VOLTAGE <= lowVoltageLimit: #si actula la proteccion cargo la Batery
            evaluate()
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tMaxStress :
            scriptSys.final_report("tMaxStress",0)
            return

        print "RUN"
        return
    except:
        scriptSys.error_report("stress_test()")
################################################################
##########                  EVALUATE                  ##########
################################################################
#Setup
iDischTest1 =   int(-1000 * float(iDischargeTest1))
iDischTest2 =   int(-1000 * float(iDischargeTest2))
iMar =       60
factor1 = 10
factor2 = 1
factor3 = 1
factor4 = 15
slope   = 9.2
origin  = 19158
def evaluate() :
    try:
        capacityVectoAmps   = 0
        capacityVectorAh    = 0
        capacityVectoWatt   = 0
        for line in scriptSys.data:
            i = int(line['CURRENT'])
            t = int(line['TIME'])
            if i >= (iDischTest1 - iMar) and i <=(iDischTest1 + iMar) \
                and (t > scriptSys.TIME_INIT):
                capacityVectoAmps += int(line['CURRENT'])
                capacityVectoWatt += int(line['CURRENT']) * int(line['VOLTAGE'])
        capacityAh = int(capacityVectoAmps / (1000*3600)) #/1000x mAmp y 3600xHr
        capacityWh = int(capacityVectoAmps / (1000000*3600))
        # scriptSys.import_data()
        result = (scriptSys.TIME - scriptSys.TIME_INIT)
        #regresion lineal
        SoH = int((result * slope + origin)/1000)
        scriptSys.final_report("sohAW",SoH,capacityAh,capacityWh)
        return
    except:
        scriptSys.error_report("evaluate()")



################################################################
##########                  ALREADY CHARGED           ##########
################################################################

#Setup
#
def already_charged(option) :
    try:
        if scriptSys.GENERAL['mode'] != 'END' : #si es llamado por primera vez
            scriptSys.GENERAL['mode'] = 'END'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "STOP,NTF,100,0"

        scriptSys.GUI['line1'] = "Analysis Finished"
        if option == 1 :
            scriptSys.GUI['line2'] = "Batery low voltage :" \
                + str(scriptSys.VOLTAGE) + 'V'
        if option == 2 :
            scriptSys.GUI['line2'] = "Batery already DISCHARGED :" \
                + str(scriptSys.VOLTAGE) + 'V'
        scriptSys.GUI['bgcolor'] = '"120,244,183"'
        scriptSys.GUI['extra_info'] = " Z1="+scriptSys.EVAL['int_z1'] \
            +" Z2="+scriptSys.EVAL['int_z2']
        scriptSys.copy_report()
        return
    except:
        scriptSys.error_report("already_charged()")
