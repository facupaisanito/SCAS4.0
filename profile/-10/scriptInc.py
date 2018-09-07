#       python.exe .\scriptInc.py --Param-scriptInc 1

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
        scriptSys.AUX['line_m'] = str(M)
        scriptSys.AUX['line_m'] = str(VAR1)
        return
    except Exception as e:
        scriptSys.error_report(e,"get_line()")
################################################################
##########                  measure_z1                ##########
################################################################
#Setup
tTest1  =   30  #tiempo de descarga suave
tTest2  =   30  #tiempo de descarga fuerte
tTest3  =   60 #tiempo de recuperacion
tTest4  =   30 #tiempo de chequeo e incio de sig etapa
tTest5  =   20
tMargin =   5   #margen de tiempo por no ser 10s exactos
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
        if scriptSys.SCRIPT['mode'] != 'Z_MEASURE' : #si es 1 llamado
            scriptSys.SCRIPT['mode'] = 'Z_MEASURE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "SQUARE,1.0,-1.0,2"
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tTestD :
            stress_test()
            return
        if  actual_time >= (tTestC- tMargin)and actual_time <(tTestC + tMargin):
            print "PAUSE"
            return
        if  actual_time >=(tTestB - tMargin)and actual_time <(tTestB + tMargin):
            print "CHARGE,4.2,1.8"
            return
        if  actual_time >=(tTestA - tMargin)and actual_time <(tTestA + tMargin):
            print "PAUSE"
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"measure_z1()")
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
        if scriptSys.SCRIPT['mode'] != 'Z_MEASURE2' : #si es llamado por 1
            scriptSys.SCRIPT['mode'] = 'Z_MEASURE2'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "DISCHARGE,1.0"
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tTestD2 :
            # deja reposar y chequea q no caiga la tension
            # final_report(0,0)
            # stress_test()
            scriptSys.SCRIPT['mode'] = 'CHARGE'
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
    except Exception as e:
        scriptSys.error_report(e,"measure_z2()")
################################################################
##########                  STRESS                    ##########
################################################################

#Setup
# tTest1  =   20  #tiempo de descarga suave
# tTest2  =   120  #tiempo de descarga fuerte
# tTest3  =   400  #tiempo de recuperacion
# tTest4  =   180 #tiempo de chequeo e incio de sig etapa
# tTest5  =   20
tTest13  =   10  #tiempo de resting
tTest23  =   270  #tiempo de descarga fuerte
# tTest23  =   30  #tiempo de descarga fuerte 2780
tTest33  =   20  #tiempo de recuperacion
# tTest33  =   10  #tiempo de recuperacion 20
tTest43  =   30 #tiempo de chequeo e incio de sig etapa
tTest53  =   20
vMargin =   16
iMargin =   16
# maxTimeInit = 20          # 10 seg
# voltageAverage = 3
# currentAverage = 5
# Z1 = 0
# Z2 = 0
tTestA3  =   tTest13
tTestB3  =   tTest13 + tTest23
tTestC3  =   tTest13 + tTest23 + tTest33
tTestD3  =   tTest13 + tTest23 + tTest33 + tTest43
iCharge1 =          '0.5'
vCharge1 =          '4.2'
iDischargeTest1 =   '1.8'
# iDischargeTest2 =   '0.5'
iDischargeTest2 =   '1.0'
lowVoltageLimit =   2500
tMaxStress =     	2000
# tMaxStress =     	4 * 60 * 60 # 4 hr
maxTimeInit =       	15          # 10 seg
#
def stress_test() :
    try:
        if scriptSys.SCRIPT['mode'] != 'STRESS' : #si es llamado por 1
            scriptSys.SCRIPT['mode'] = 'STRESS'
            scriptSys.TIME_INIT = scriptSys.TIME
            scriptSys.AUX['testnr'] = str(int(scriptSys.AUX['testnr'])+1)
            scriptSys.AUX['strike'] = 0
            scriptSys.AUX['strikeh'] = 0
            print "PAUSE"
            return
        #condiciones de Fallas:
        if scriptSys.VOLTAGE < lowVoltageLimit : #si actula la proteccion cargo la Batery
            scriptSys.AUX['Dropdown voltage T='+ str(scriptSys.TIME)] =scriptSys.VOLTAGE
            scriptSys.send_msg('Dropdown voltage T='+ str(scriptSys.TIME))
            scriptSys.final_report("SoHfail",0)
            return
        # if scriptSys.VOLTAGE < vMargin : #si actula la proteccion cargo la Batery
        #     scriptSys.SCRIPT['mode'] = 'CHARGE'
        #     scriptSys.TIME_INIT = scriptSys.TIME
        #     print "CHARGE,"+ vCharge1 +","+ iCharge1
        #     return
        if scriptSys.CURRENT > (-iMargin) and scriptSys.VOLTAGE < vMargin :
            scriptSys.AUX['F12'] =scriptSys.CURRENT
            scriptSys.final_report("F12",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeInit:
            slope1 = scriptSys.get_slope(range(scriptSys.TIME_INIT + 3,scriptSys.TIME))
            if slope1['VOLTAGE']  > 80 and slope1['CURRENT'] > 180 :
                scriptSys.AUX['F13 T='+ str(scriptSys.TIME)] =slope1
                scriptSys.send_msg('F13 T='+ str(scriptSys.TIME))
                scriptSys.final_report("F13",0)
                return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= tMaxStress:
            scriptSys.AUX['F12'] =(scriptSys.TIME - scriptSys.TIME_INIT)
            scriptSys.final_report("F15",0)
            return
        ######################################

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        scriptSys.AUX['actual_time'] = actual_time
        if  actual_time >= (tTestC3- tMargin)and actual_time <(tTestC3 + tMargin):
            msj = evaluate()
            return
        if  actual_time >=(tTestB3 - tMargin)and actual_time <(tTestB3 + tMargin):
            print "PAUSE"
            return
        if  actual_time >=(tTestA3 - tMargin)and actual_time <(tTestA3 + tMargin):
            print "DISCHARGE,"+ iDischargeTest2
            return

        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"stress_test()")
################################################################
##########                  EVALUATE                  ##########
################################################################
#Setup
Boundary = 70
Bmargin = 5
iDischTest1 =   int(-1000 * float(iDischargeTest1))
iDischTest2 =   int(-1000 * float(iDischargeTest2))
iMar =       60
factor1 = 1
factor2 = 0
factor3 = 1
factor4 = 15
slopeP   = -194
org  = 90000
def evaluate() :
    try:
        scriptSys.import_data()
        scriptSys.data = scriptSys.data[10:-10]
        i = []
        for line in scriptSys.data:
            i.append(int(line['I0']))
        w = 20
        for x in range(w+1,len(i)):
            iavew = sum(i[x-w:x-1])/float(len(i[x-w:x-1]))
            if (iavew - i[x]) > 100 :
                scriptSys.AUX['failcode'] = 1
                return 'FAIL'
        iave = sum(i)/float(len(i))
        if iave < 600 and iave > 400:
            scriptSys.AUX['failcode'] = 2
            return 'FAIL'
        if iave < 200:
            scriptSys.AUX['failcode'] = 3
            return 'FAIL'
        return 'OK'

    except Exception as e:
        scriptSys.error_report(e,"evaluate()")
################################################################
##########                  evaluate_rt                  ##########
################################################################

def evaluate_rt() :
    try:
        return 'OK'
    except Exception as e:
        scriptSys.error_report(e,"evaluatert()")
################################################################
##########                  ALREADY CHARGED           ##########
################################################################

#Setup
#
def already_charged(option) :
    try:
        if scriptSys.SCRIPT['mode'] != 'END' : #si es llamado por primera vez
            scriptSys.SCRIPT['mode'] = 'END'
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
    except Exception as e:
        scriptSys.error_report(e,"already_charged()")


################################################################
##########                  ALREADY CHARGED           ##########
################################################################
def measure() :
    try:
        if scriptSys.SCRIPT['mode'] != 'MEASURE' : #si es llamado por primera vez
            scriptSys.SCRIPT['mode'] = 'MEASURE'
            scriptSys.TIME_INIT = scriptSys.TIME
            scriptSys.ANALYSIS['analysisstate'] = 'RUNNING'
            # return 'DONE'

        ######
        # condiciones de carga del telefono
        ######
        if evaluate_rt() == 'FAIL':
            scriptSys.AUX['failcode']
            return 'FAIL'
        print 'RUN'
        return 'DONE'
    except Exception as e:
        scriptSys.error_report(e,"measure()")
################################################################
##########                  ALREADY CHARGED           ##########
################################################################
def analysis() :
    try:
        if scriptSys.SCRIPT['mode'] != 'ANALYSIS' : #si es llamado por primera vez
            scriptSys.SCRIPT['mode'] = 'ANALYSIS'
            scriptSys.TIME_INIT = scriptSys.TIME

        if evaluate() == 'OK':
            scriptSys.ANALYSIS['analysisstate'] = 'OK'
        else:
            scriptSys.ANALYSIS['analysisstate'] = 'FAIL'

        return 'DONE'

    except Exception as e:
        scriptSys.error_report(e,"analysis()")
################################################################
##########                  ALREADY CHARGED           ##########
################################################################
maxTimeErase = 3 * 60   #3 min
def erase() :
    try:
        if scriptSys.SCRIPT['mode'] != 'ERASE' : #si es llamado por primera vez
            scriptSys.SCRIPT['mode'] = 'ERASE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "ERASE"
            return 'NO'
        if scriptSys.ANALYSIS['erasestate'] == 'OK' :
            return 'DONE'
        if scriptSys.ANALYSIS['erasestate'] == 'FAIL' :
            return 'DONE'
        # scriptSys.send_msg(str((scriptSys.TIME - scriptSys.TIME_INIT)))
        if scriptSys.ANALYSIS['erasestate'] == 'RUNNING' or scriptSys.ANALYSIS['erasestate'] == 'NO'  :
            if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeErase:
                scriptSys.ANALYSIS['erasestate'] = 'FAIL'
                return 'DONE'
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"erase()")
################################################################
##########                  ALREADY CHARGED           ##########
################################################################
maxTimeInform = 60
def inform() :
    try:
        if scriptSys.SCRIPT['mode'] != 'INFORM' : #si es llamado por primera vez
            scriptSys.SCRIPT['mode'] = 'INFORM'
            scriptSys.TIME_INIT = scriptSys.TIME

            if scriptSys.DEV['datastate'] == 'OK':
                if scriptSys.ANALYSIS['erasestate'] == 'OK' :
                    if scriptSys.ANALYSIS['analysisstate'] == 'OK':
                        scriptSys.final_report('SUCCESS_A',0)
                    elif scriptSys.ANALYSIS['analysisstate'] == 'FAIL':
                        scriptSys.final_report('FAIL_A',int(scriptSys.AUX['failcode']))
                    else:
                        scriptSys.final_report('FAIL_Z',int(scriptSys.AUX['failcode']))
                elif scriptSys.ANALYSIS['erasestate'] == 'FAIL' :
                    if scriptSys.ANALYSIS['analysisstate'] == 'OK':
                        scriptSys.final_report('FAIL_B',0)
                    elif scriptSys.ANALYSIS['analysisstate'] == 'FAIL':
                        scriptSys.final_report('FAIL_C',int(scriptSys.AUX['failcode']))
                    else:
                        scriptSys.final_report('FAIL_Y',int(scriptSys.AUX['failcode']))
            elif scriptSys.DEV['datastate'] == 'FAIL' :
                if scriptSys.ANALYSIS['analysisstate'] == 'OK':
                    scriptSys.final_report('FAIL_D',0)
                elif scriptSys.ANALYSIS['analysisstate'] == 'FAIL':
                    scriptSys.final_report('FAIL_E',int(scriptSys.AUX['failcode']))
                else:
                    scriptSys.final_report('FAIL_X',int(scriptSys.AUX['failcode']))
            else:
                scriptSys.final_report('FAIL_W',int(scriptSys.AUX['failcode']))
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeInform:
            print "STOP"
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"inform()")
