#-----------------------------------------------------------------------
# ScriptTest  for BA
# Version: 12
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------

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
    print "ERROR file scriptSys Not found in scriptTest!!"
    sys.exit()
try:
    sys.argv.append('--Param-scriptInc')
    sys.argv.append(sys.argv[1])
    import scriptInc
except:
    print "ERROR file scriptInc Not found in scriptTest!!"
    sys.exit()
for px in sys.argv:
    if px == '-d':
        scriptSys.DEBUG_MODE = True
        try:
            sys.argv.append('--Param-scriptDebug')
            sys.argv.append(sys.argv[1])
            import scriptDebug
        except:
            print "ERROR file scriptDebug Not found in scriptTest!!"
            sys.exit()

################################################################
##########                  SETUP                     ##########
################################################################
umbralVoltTarget =  	4100
umbralCurrentTarget =   400
umbralVoltHigh =    	umbralVoltTarget
umbralVoltLow =     	3200
umbralVolt =        	umbralVoltTarget * 0.03
maxTimeInit =       	15          # 10 seg
maxTimeTest =           7 * 60 * 60 #  hr
maxTimeDischarge =  	4 * 30 * 60     # hr
minTimeDischarge =  	60
maxTimeChargeHig =     	1 * 60 * 60 #  hr
maxTimeChargeMed =     	2 * 60 * 60 #  hr
maxTimeChargeLow =     	4 * 60 * 60 #  hr
minTimeCharge =     	5 * 60
maxTimeCond =       	45          # 10 seg
tMargin =               3
vMargin =               16
iMargin =               16
iCharge1 =          	'0.5'
iCharge2 =          	'1.8'
iCharge3 =          	'1.3'
iCharge4 =          	'1.0'
vCharge1 =          	'4.1'
vCharge2 =          	'4.2'
vCharge3 =          	'4.1'
vCharge4 =          	'4.2'
iDischarge1 =       	'1.6'
iDischarge2 =       	'1.3'
iDischarge3 =       	'1.0'
iDischarge4 =       	'0.5'
VALTA   = 3800
VBAJA   = 3200
################################################################
##########                  TEST                      ##########
################################################################
if int(scriptSys.GENERAL['entradas']) < 3:
    print "RUN"
    sys.exit()
if int(scriptSys.GENERAL['entradas']) == 3:
    print "DATA"
    sys.exit()
if int(scriptSys.GENERAL['entradas']) > 3:
    if scriptSys.EVAL['erasestate'] == 'NO':
        print "RUN"
        sys.exit()
    if scriptSys.EVAL['erasestate'] == 'OK':
        scriptSys.EVAL['success'] = "NTF"
    if scriptSys.EVAL['erasestate'] == 'FAIL':
        scriptSys.EVAL['success'] = "FAIL"
    print "STOP"
    scriptSys.ini_Update()
    sys.exit()
################################################################
##########                  INIT                      ##########
################################################################
def init_state() :
    try:
        if int(scriptSys.TIME) >= maxTimeInit :
            if scriptSys.VOLTAGE > VALTA :scriptSys.GENERAL['vstate'] = "vALTA"
            if scriptSys.VOLTAGE < VBAJA :scriptSys.GENERAL['vstate'] = "vBAJA"
            else :                        scriptSys.GENERAL['vstate'] = "vMEDIA"

            if scriptSys.CURRENT >iMargin or scriptSys.CURRENT < (-iMargin):
                scriptSys.final_report("F01",0)
                return
            if scriptSys.CURRENT < (2*iMargin):
                charge_state(0)
                return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"init_state()")
################################################################
##########                  CHARGE                    ##########
################################################################
def charge_state(number) :
    try:
        if not scriptSys.GENERAL['mode'] == 'CHARGE' : #si es llamado por 1 vez
            scriptSys.GENERAL['mode'] = 'CHARGE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "CHARGE,"+ vCharge1 +","+ iCharge1
            return
        if scriptSys.CURRENT < iMargin and \
            scriptSys.VOLTAGE > (int(1000*float(vCharge2))-100) :
            scriptSys.final_report("F03",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) <= maxTimeInit:
            print "CHARGE,"+ vCharge2 +","+ iCharge2
            return
        if  scriptSys.CURRENT < (umbralCurrentTarget) and \
            (scriptSys.TIME - scriptSys.TIME_INIT) >= minTimeCharge:
            cond_state()
            return

        #condiciones de Fallas:

        if scriptSys.CURRENT < iMargin :
            scriptSys.final_report("F02",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeInit:
            slope = scriptSys.get_slope(range(scriptSys.TIME_INIT + 3,scriptSys.TIME))
            if scriptSys.GENERAL['vstate'] == "vBAJA" and not slope['VOLTAGE'] > -80 \
                and scriptSys.CURRENT > (int(1000*float(iCharge2))-200):
                scriptSys.final_report("F04",0)
                return
            if scriptSys.GENERAL['vstate'] == "vMEDIA" and not slope['VOLTAGE'] > -80\
                and scriptSys.CURRENT > (int(1000*float(iCharge2))-200):
                scriptSys.final_report("F05",0)
                return
            if scriptSys.GENERAL['vstate'] == "vALTA" and not slope['CURRENT'] < 80\
                and scriptSys.VOLTAGE > (int(1000*float(vCharge2))-200):
                scriptSys.final_report("F06",0)
                return
            if slope['VOLTAGE'] > 0 and slope['CURRENT'] < 80 :
                scriptSys.final_report("F07",0)
                return
            if slope['VOLTAGE'] < 100 :
                scriptSys.final_report("F08",0)
                return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeChargeLow and \
            scriptSys.GENERAL['vstate'] == "vBAJA" :
            scriptSys.final_report("F09",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeChargeMed and \
            scriptSys.GENERAL['vstate'] == "vMEDIA" :
            scriptSys.final_report("F10",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeChargeHig and \
            scriptSys.GENERAL['vstate'] == "vALTA" :
            scriptSys.final_report("F11",0)
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"charge_state()")
################################################################
##########                  DISCHARGE                 ##########
################################################################
def discharge_state(number) :
    try:
        if not scriptSys.GENERAL['mode'] == 'DISCHARGE' : #si es llamado por 1
            scriptSys.GENERAL['mode'] = 'DISCHARGE'
            scriptSys.TIME_INIT = scriptSys.TIME
            if number == 1 : print "DISCHARGE,"+ iDischarge1
            if number == 2 : print "DISCHARGE,"+ iDischarge2
            if number == 3 : print "DISCHARGE,"+ iDischarge3
            return

        if scriptSys.VOLTAGE < (umbralVoltTarget - umbralVolt) \
            and (scriptSys.TIME - scriptSys.TIME_INIT) >= minTimeDischarge:
            cond_state()
            return
        #condiciones de Fallas:
        if scriptSys.CURRENT > (-iMargin) and scriptSys.VOLTAGE < vMargin :
            scriptSys.final_report("F12",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeInit:
            slope = scriptSys.get_slope(range(scriptSys.TIME_INIT + 3,scriptSys.TIME))
            if slope['VOLTAGE']  > 80 and slope['CURRENT'] > 180 :
                scriptSys.final_report("F13",0)
                return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeDischarge:
            scriptSys.final_report("F15",0)
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"discharge_state()")
################################################################
##########                  CONDITIONING               #########
################################################################
def cond_state():
    try:
        if not scriptSys.GENERAL['mode'] == 'CONDITIONING' : #es llamado por 1
            scriptSys.GENERAL['mode'] = 'CONDITIONING'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "PAUSE"
            return

        if  ((scriptSys.TIME) - (scriptSys.TIME_INIT)) >= (maxTimeCond-tMargin):
            stress_state()
            return

        #condiciones de Fallas:
        if scriptSys.CURRENT > (-iMargin) and scriptSys.VOLTAGE < vMargin :
            scriptSys.final_report("F18",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeInit:
            slope = scriptSys.get_slope(range(scriptSys.TIME_INIT + 3,scriptSys.TIME))
            if slope['VOLTAGE']  < -180 :
                print slope
                scriptSys.final_report("F19",0)
                return
        if scriptSys.CURRENT >iMargin or scriptSys.CURRENT < (-iMargin):
            print scriptSys.CURRENT
            scriptSys.final_report("F20",0)
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"cond_state()")
################################################################
##########                  Z_MEASURE                 ##########
################################################################
def zmeasure_state() :
    try:
        scriptInc.measure_z1()
        return
    except Exception as e:
        scriptSys.error_report(e,"zmeasure_state()")
################################################################
##########                  Z_MEASURE                 ##########
################################################################
def zmeasure2_state() :
    try:
        scriptInc.measure_z2()
        return
    except Exception as e:
        scriptSys.error_report(e,"zmeasure2_state()")
################################################################
##########                  STRESS                     ##########
################################################################
def stress_state():
    try:
        scriptInc.stress_test()
        return
    except Exception as e:
        scriptSys.error_report(e,"stress_state()")
################################################################
##########                  PAUSE                     ##########
################################################################
def pause_state():
    try:
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"pause_state()")
################################################################
##########                  END                       ##########
################################################################
def end_state():
    try:
        scriptSys.GENERAL['mode']= "STOP"
        scriptSys.TIME_INIT = scriptSys.TIME
        print "STOP"
        # scriptSys.copy_report()
        return
    except Exception as e:
        scriptSys.error_report(e,"end_state()")


# print "SET,4.2,1.0,1.2"
# print "SET"
# print "STOP"
# print "STOP,NTF"
# print "`STOP,FAIL,150,68"`
# print "STOP,DCC,0,"+str(z)
# print "CHARGE"
# print "CHARGE,4.2,0.8"
# print "DISCHARGE"
# print "DISCHARGE,1.2"
# print "PAUSE"
# print "FIND"
# print "DISABLE"
# print "ENABLE"

################################################################
################################################################
##########                  MAIN                      ##########
################################################################
################################################################
if scriptSys.Msg == 81 :
    scriptSys.final_report("F22",0)
    sys.exit()
if  scriptSys.GENERAL['mode'] == "INIT":
    init_state()
elif scriptSys.GENERAL['mode'] == "CHARGE":
    charge_state(1)
elif scriptSys.GENERAL['mode'] == "DISCHARGE":
    discharge_state(1)
elif scriptSys.GENERAL['mode'] == "CONDITIONING":
    cond_state()
elif scriptSys.GENERAL['mode'] == "Z_MEASURE":
    zmeasure_state()
elif scriptSys.GENERAL['mode'] == "Z_MEASURE2":
    zmeasure2_state()
elif scriptSys.GENERAL['mode'] == "STRESS":
    stress_state()
elif scriptSys.GENERAL['mode'] == "PAUSE":
    pause_state()
elif scriptSys.GENERAL['mode'] == "END":
    end_state()
scriptSys.ini_Update()
if (scriptSys.TIME - scriptSys.TIME_INIT) > maxTimeTest:
    scriptSys.final_report("F21",0)
sys.exit()
