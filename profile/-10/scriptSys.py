#       python.exe .\scriptSys.py --Param-scriptSys 1
#-----------------------------------------------------------------------
# ScriptSys  for BA
# Version: 1
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------
DEBUG_MODE = False
try:
    import sys,os
except:
    print "import sys,os in scriptSys Not found!!"
    sys.exit()
try:
    import ConfigParser
except:
    print "import configparser in scriptSys Not found!!"
    sys.exit()
try:
    import csv
except:
    print "import CSV in scriptSys Not found!!"
    sys.exit()
for px in sys.argv:
    if px == '-d':
        DEBUG_MODE = True
        try:
            sys.argv.append('--Param-scriptDebug')
            sys.argv.append(sys.argv[1])
            import scriptDebug
        except:
            print "ERROR file scriptDebug Not found!!"
            sys.exit()
for px in sys.argv:
    if px == '--Param-scriptSys':
        idx = sys.argv.index(px)
        sys.argv.pop(idx) # remove option
        STATION_N = sys.argv[idx]
        sys.argv.pop(idx) # remove value

config = ConfigParser.ConfigParser()

PATH = 'data/st'
if DEBUG_MODE : PATH = '../../data/st'
GENERAL = {}
SCRIPT = {}
GUI = {}
DEV = {}
MENSSAGE = {}
AUX = {}
ANALYSIS = {}
TIME_INIT = 0
VOLTAGE = 0
CURRENT = 0
TIME = 0
Msg = 0
#####################################################
#####################################################
#Funciones basicas
#####################################################
#####################################################
def ini_Update ():
    try:

        SCRIPT['time'] = str(TIME)
        SCRIPT['time_init'] = str(TIME_INIT)
        SCRIPT['voltage'] = str(VOLTAGE)


        for option in GENERAL:
            config.set('General',option,GENERAL[option])
        for option in SCRIPT:
            config.set('Script',option,SCRIPT[option])
        for option in GUI:
            config.set('GUI',option,GUI[option])
        for option in ANALYSIS:
            config.set('Analyzis',option,ANALYSIS[option])
        for option in DEV:
            config.set('Dev',option,DEV[option])
        for option in MENSSAGE:
            config.set('Msg',option,MENSSAGE[option])
        for option in AUX:
            config.set('AUX',option,AUX[option])
        with open(PATH+STATION_N+'.ini', 'w') as configfile:
            config.write(configfile)


        return
    except Exception as e:
        # print "STOP,FAIL,0,0"
        print "Script ERROR:ini_Update()"
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    return
################################################################
##########                  ERROR REPORT              ##########
################################################################
def error_report(e,string):
    try:
        print "STOP"

        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        # print "Script ERROR: " + str(string)
        # err = str('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        #
        GUI['line1'] = "Script ERROR: "+ str(string)
        GUI['line2'] = ""
        GUI['bgcolor'] = '"244,10,10"'
        GUI['extra_info'] = " TIME="+str(TIME)+" Tinit="+str(TIME_INIT)
        ini_Update()
    except Exception as e:
        print "error_report() ERROR"
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    return
################################################################
##########                  COPY REPORT               ##########
################################################################
def copy_report() :
    try:
        try:
            with open(PATH + STATION_N + ".csv", "rb") as ifile:
                ifile.readline()
                name = ifile.readline()
                name = name.replace(" ","_")
                name = name.replace(",","_")
                name = name.replace(".","")
                name = name.replace(":","-")
                name = name[:-12]
                reader = csv.reader(ifile)
                dato = []
                for row in reader:
                    dato.append(row)
            ifile.close()
        except:
            print "el copy no funciono csv1"
        file_path = "historial/"+ name
        directory = os.path.dirname(file_path)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)
        try:
            myFile = open( file_path +".csv", 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(dato)
            myFile.close()
        except:
            print "Create /historal folder!!!"
        try:
            with open(PATH + STATION_N + ".ini", "rb") as ifile:
                reader = csv.reader(ifile)
                dato = []
                for row in reader:
                    dato.append(row)
            ifile.close()
        except:
            print "el copy no funciono csv1"
        try:
            myFile = open(file_path +".ini", 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(dato)
            myFile.close()
        except:
            print "el copy no funciono csv2"
        try:
            with open(PATH + STATION_N + ".log", "rb") as ifile:
                reader = csv.reader(ifile)
                dato = []
                for row in reader:
                    dato.append(row)
            ifile.close()
        except:
            print "lectura del log fallo"
        try:
            myFile = open(file_path +".log", 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(dato)
            myFile.close()
        except:
            print "escritura del log fallo"
        #
        return
    except Exception as e:
        error_report(e,"copy_report()")
################################################################
##########                  SEND MESSAGE              ##########
################################################################
def send_msg(string) :
    try:
        MENSSAGE['type'] = "warning"
        MENSSAGE['time'] = "60"
        MENSSAGE['txt'] = string
        # return
        ini_Update()
        return
    except Exception as e:
        error_report(e,"send_msg()")
################################################################
##########                  FINAL REPORT              ##########
################################################################
def final_report(mode, *value) :
    try:
        if mode == 0 :
            print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "---"
            GUI['bgcolor'] = '"100,100,100"'
            GUI['extra_info'] = value


        if mode == "SUCCESS_A" :
            # print "STOP"
            ANALYSIS['evalcode'] = 'SUCCESS_A'
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"51,204,51"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_A" :
            # print "STOP"
            ANALYSIS['evalcode'] = 'FAIL_A'+str(AUX['failcode'])
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_B" :
            ANALYSIS['evalcode'] = 'FAIL_B'
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_C" :
            ANALYSIS['evalcode'] = 'FAIL_C'+str(AUX['failcode'])
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_D" :
            ANALYSIS['evalcode'] = 'FAIL_D'
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,161,0"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_E" :
            ANALYSIS['evalcode'] = 'FAIL_E'+str(AUX['failcode'])
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"

        if mode == "FAIL_W" :
            ANALYSIS['evalcode'] = 'FAIL_W'+str(AUX['failcode'])
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_X" :
            ANALYSIS['evalcode'] = 'FAIL_X'+str(AUX['failcode'])
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_Y" :
            ANALYSIS['evalcode'] = 'FAIL_Y'+str(AUX['failcode'])
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"
        if mode == "FAIL_Z" :
            ANALYSIS['evalcode'] = 'FAIL_Z'+str(AUX['failcode'])
            # print "STOP"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = ANALYSIS['evalcode']
            GUI['line3'] = "Erase: " + str(ANALYSIS['erasestate'])
            GUI['bgcolor'] = '"255,102,255"'
            GUI['extra_info'] = "none"

        # return
    except Exception as e:
        error_report(e,"final_report()")
    ini_Update()
    copy_report()
    return
################################################################
##########                  import_data                ##########
################################################################
data = []
def import_data():
    try:
        with open(PATH +STATION_N+".csv",'rb') as f:
            f.readline()
            f.readline()
            reader = csv.DictReader(f, delimiter=',')
            holes = 0
            for row in reader: data.append(row)
            for row in data:
                ind = data.index(row) + 1
                if row['TIME'] == data[-1]['TIME'] : break
                delta = int(data[ind]['TIME']) - int(row['TIME'])
                deltaV = int(data[ind]['V0']) - int(row['V0'])
                deltaI = int(data[ind]['I0']) - int(row['I0'])
                # deltaT = int(data[ind]['TEMP']) - int(row['TEMP'])
                if delta > 1:
                    holes = holes + 1
                    dV=deltaV/delta
                    dI=deltaI/delta
                    dT=deltaT/delta
                    temp = {}
                    for x in row:
                        temp[x] = row[x]
                    temp['TIME'] = str(int(row['TIME'])+1)
                    temp['V0'] = str(int(row['V0'])+dV)
                    temp['I0'] = str(int(row['I0'])+dI)
                    # temp['TEMP'] = str(int(row['TEMP'])+dT)
                    data.insert(ind,temp)
        AUX['holes'] = str(holes)
        return
    except Exception as e:
        error_report(e,"import_data()")
################################################################
##########                  get_data                ##########
################################################################
def get_data(dType, tLapse):
    try:
        if len(data) <= 1 :
            import_data()   #Comprueba que este cargado el csv

        if 'list' in str(type(tLapse)):
            info = []
            for x in tLapse :
                var = [int(row[dType]) for row in data if int(row['TIME']) == x]
                info.append(var[0])
        else :
            info = [int(row[dType]) for row in data if int(row['TIME']) == tLapse]
            return info[0]
        return info
    except Exception as e:
        error_report(e,"get_data()")
################################################################
##########                  get_slope                ##########
################################################################
def get_slope(tLapse):
    try:
        v = get_data("V0",tLapse)
        i = get_data("I0",tLapse)
        t = get_data("TEMP",tLapse)
        dI1 =0
        for a in range(len(i)-1):
            dI1 += i[a+1] - i[a]
        iSlope = ( 1000* dI1) / len(i)
        dV1 =0
        for a in range(len(v)-1):
            dV1 += v[a+1] - v[a]
        vSlope = ( 1000* dV1) / len(v)
        dt1 =0
        for a in range(len(t)-1):
            dt1 += t[a+1] - t[a]
        tSlope = ( 1000* dt1) / len(t)
        slope = {"VOLTAGE":vSlope ,"CURRENT": iSlope ,"TEMP": tSlope}

        #############
        # sys.stdout=open("output.txt","w")
        # print "t:"+str(TIME)
        # print v
        # print tLapse
        # print slope
        # sys.stdout.close()
        ##########################
        return slope
    except Exception as e:
        scriptSys.error_report(e,"get_slope()")

################################################################
##########                  get_data                ##########
################################################################
def import_ini( STATION_N ):
    try:
        try: config.read(PATH +STATION_N+".ini")
        except : print "no read .ini"
        sections = config.sections()

        if not 'General' in sections :
            config.add_section('General')

        if not 'Script' in sections :
            config.add_section('Script')
        options = config.options('Script')
        if not 'time' in options :
            config.set('Script','time','')
        if not 'mode' in options :
            config.set('Script','mode','INIT')
        if not 'time_init' in options :
            config.set('Script','time_init','0')
        if not 'voltage' in options :
            config.set('Script','voltage','')
        if not 'vstate' in options :
            config.set('Script','vstate','')

        if not 'Analyzis' in sections :
            config.add_section('Analyzis')
        options = config.options('Analyzis')
        if not 'entradas' in options :
            config.set('Analyzis','entradas','')
        if not 'scriptstatus' in options :
            config.set('Analyzis','scriptstatus','')
        if not 'guistatus' in options :
            config.set('Analyzis','guistatus','')
        if not 'guielapsetime' in options :
            config.set('Analyzis','guielapsetime','')
        if not 'erasestate' in options :
            config.set('Analyzis','erasestate','')
        if not 'analysisstate' in options :
            config.set('Analyzis','analysisstate','')
        if not 'evalcode' in options :
            config.set('Analyzis','evalcode','')
        if not 'error' in options :
            config.set('Analyzis','error','')

        if not 'GUI' in sections :
            config.add_section('GUI')
        options = config.options('GUI')
        if not 'line1' in options :
            config.set('GUI','line1','')
        if not 'line2' in options :
            config.set('GUI','line2','')
        if not 'line3' in options :
            config.set('GUI','line3','')
        if not 'bgcolor' in options :
            config.set('GUI','bgcolor','')
        if not 'extra_info' in options :
            config.set('GUI','extra_info','')

        if not 'Dev' in sections :
            config.add_section('Dev')
        options = config.options('Dev')
        if not 'datastate' in options :
            config.set('Dev','datastate','')
        if not 'battery' in options :
            config.set('Dev','battery','')

        if not 'Msg' in sections :
            config.add_section('Msg')
        options = config.options('Msg')
        if not 'type' in options :
            config.set('Msg','type','')
        if not 'time' in options :
            config.set('Msg','time','')
        if not 'txt' in options :
            config.set('Msg','txt','')

        if not 'AUX' in sections :
            config.add_section('AUX')
        options = config.options('AUX')
        # if not 'line_m' in options :
        #     config.set('AUX','line_m','')
        # if not 'line_b' in options :
        #     config.set('AUX','line_b','')
        # if not 'testnr' in options :
        #     config.set('AUX','testnr','0')
        # config.write(config)
        # config.close()
        try:
            with open(PATH + STATION_N + '.ini', 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            print "config.write(configfile) ERROR"
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        for option in config.options('General'):
            GENERAL[option]=config.get('General',option)
        for option in config.options('Script'):
            SCRIPT[option]=config.get('Script',option)
        for option in config.options('Analyzis'):
            ANALYSIS[option]=config.get('Analyzis',option)
        for option in config.options('GUI'):
            GUI[option]=config.get('GUI',option)
        for option in config.options('Dev'):
            DEV[option]=config.get('Dev',option)
        for option in config.options('Msg'):
            MENSSAGE[option]=config.get('Msg',option)
        for option in config.options('AUX'):
            AUX[option]=config.get('AUX',option)
        return
    except Exception as e:
        error_report(e,"import_ini()")

#####################################################
#####################################################
##      Abro el stXX.ini                           ##
#####################################################
#####################################################
def openini():
    try:
        try:
            import_ini(STATION_N)
            try :   TIME_INIT = int(SCRIPT['time_init'])
            except : TIME_INIT = 0

        except :
            print "ERROR "+"st"+STATION_N+".ini"+ " Not found!! in scriptSys.py"
            sys.exit()
    except Exception as e:
        error_report(e,"openini()")
#####################################################
#####################################################
##      Abro el stXX.csv                          ##
#####################################################
#####################################################

def opencsv():
    global TIME
    global VOLTAGE
    global CURRENT
    global TIME_INIT

    try:
        with open(PATH + STATION_N + ".csv",'rb') as f:
            f.readline()
            f.readline()
            reader = csv.DictReader(f, delimiter=',')
            header = reader.fieldnames
            try:
                try:
                    lastlines = list(reader)[-10:]
                except :
                    lastlines = list(reader)[-9:]
                last3lines = lastlines
                voltage = int(last3lines[0]['V0'])
                voltage += int(last3lines[1]['V0'])
                voltage += int(last3lines[2]['V0'])
                VOLTAGE = voltage/3
                current = int(last3lines[0]['I0'])
                current += int(last3lines[1]['I0'])
                current += int(last3lines[2]['I0'])
                CURRENT = current/3
                # CURRENT += int(last3lines[2]['I0'])
                TIME = int(last3lines[2]['TIME'])
                SCRIPT['voltage'] = str(voltage/3)
                #tension instantanea (en promedio de las ultimas 3 mediciones)
                SCRIPT['time'] = last3lines[2]['TIME']
                #tiempo en seg de la ultima vez q se tomo registro

            except :
                CURRENT = 0
                VOLTAGE = 0
                TIME = 0
                SCRIPT['voltage'] = VOLTAGE
                SCRIPT['time'] = TIME
            if TIME <= 15 : #asume primera entrada
                ANALYSIS['entradas'] = '0'
                SCRIPT['mode'] = 'INIT'
                TIME_INIT = 0
                GUI['line1'] = ''
                GUI['line2'] = ''
                GUI['bgcolor'] = ''
                GUI['extra_info'] = ''

            try :    ANALYSIS['entradas'] = str(int(ANALYSIS['entradas'])+1)
            except : ANALYSIS['entradas'] = "1.0"
            # with open(PATH + STATION_N + ".csv",'rb') as f:
            #     f.readline()
            #     f.readline()
            #     reader = csv.DictReader(f, delimiter=',')
            # header = reader.fieldnames

        ini_Update()
        return
    except Exception as e:
        error_report(e,"openini()")


#####################################################
#####################################################
##              MAIN                               ##
#####################################################
#####################################################
