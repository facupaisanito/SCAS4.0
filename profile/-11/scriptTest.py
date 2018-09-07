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
umbralCurrentTarget =   300
umbralVoltHigh =    	umbralVoltTarget
umbralVoltLow =     	3800
umbralVolt =        	umbralVoltTarget * 0.03
# maxTimeInit =       	2 * 60          # 2min
maxTimeInit =       	20          # 2min
maxTimeTest =           2 * 60 * 60 #  hr
# maxTimeMeasure =        5 * 60
maxTimeMeasure =        30
# maxTimeTest =           2000 #  hr
maxTimeDischarge =  	30 * 60     # 30 min
minTimeDischarge =  	60
maxTimeChargeHig =     	1 * 60 * 60 #  hr
maxTimeChargeMed =     	2 * 60 * 60 #  hr
maxTimeChargeLow =     	4 * 60 * 60 #  hr
minTimeCharge =     	5 * 60
maxTimeCond =       	45          # 10 seg
tMargin =               3
vMargin =               16
iMargin =               20
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
##########                  INIT                      ##########
################################################################
def init_state() :
    try:
        if int(scriptSys.TIME) >= maxTimeInit :
            #condiciones inciales:
            if scriptSys.CURRENT < (iMargin):
                scriptSys.AUX['failcode'] = 3
                scriptSys.final_report('FAIL_A',int(scriptSys.AUX['failcode']))
                return
            ##############################
            measure_state()
            return
            ##############################
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"init_state()")


################################################################
##########                  MEASURE                 ##########
################################################################
def measure_state() :
    try:
        if scriptSys.TIME < maxTimeMeasure:
            if scriptInc.measure() == 'FAIL':
                erase_state()
        else:
            analysis_state()
        # print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"zmeasure_state()")
################################################################
##########                  analysis                  ##########
################################################################
def analysis_state() :
    try:
        if scriptInc.analysis() == 'DONE':
            erase_state()
        return
    except Exception as e:
        scriptSys.error_report(e,"zmeasure2_state()")
################################################################
##########                  erase                     ##########
################################################################
def erase_state():
    try:
        if scriptInc.erase() == 'DONE':
            inform_state()
        return
    except Exception as e:
        scriptSys.error_report(e,"stress_state()")
################################################################
##########                  PAinform                  ##########
################################################################
def inform_state():
    try:
        scriptInc.inform()
        return
    except Exception as e:
        scriptSys.error_report(e,"pause_state()")
################################################################
##########                  END                       ##########
################################################################
def end_state():
    try:
        scriptSys.SCRIPT['mode']= "STOP"
        scriptSys.TIME_INIT = scriptSys.TIME
        print "STOP"
        # scriptSys.copy_report()
        return
    except Exception as e:
        scriptSys.error_report(e,"end_state()")


################################################################
################################################################
##########                  MAIN                      ##########
################################################################
################################################################
scriptSys.openini()
scriptSys.opencsv()
if  scriptSys.SCRIPT['mode'] == "INIT":
    init_state()
elif scriptSys.SCRIPT['mode'] == "MEASURE":
    measure_state()
elif scriptSys.SCRIPT['mode'] == "ANALYSIS":
    analysis_state()
elif scriptSys.SCRIPT['mode'] == "ERASE":
    erase_state()
elif scriptSys.SCRIPT['mode'] == "INFORM":
    inform_state()
elif scriptSys.SCRIPT['mode'] == "PAUSE":
    pause_state()
elif scriptSys.SCRIPT['mode'] == "END":
    end_state()
scriptSys.ini_Update()
if (scriptSys.TIME - scriptSys.TIME_INIT) > maxTimeTest:
    scriptSys.AUX['F21'] =scriptSys.CURRENT
    scriptSys.AUX['F04t'] =scriptSys.TIME
    scriptSys.final_report("F21",0)
sys.exit()
