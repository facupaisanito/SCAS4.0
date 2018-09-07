# Taking care of jupyter environment
# show graphs in-line, and turn on/off pretty_printing of lists
# %matplotlib inline
# %pprint
import plotly
import plotly.graph_objs as go
import numpy as np   # So we can use random numbers in examples
import csv
import sys
# import operator
# import numbers
try:
    sys.argv.append('--Param-scriptSys')
    sys.argv.append(sys.argv[1])
    import scriptSys
except:
    print "ERROR file scriptSys Not found!!"
    sys.exit()
print "\n\n\n--------------------- DEBUG MODE ---------------------\n\n\n"

for px in sys.argv:
    if px == '--Param-scriptDebug':
        idx = sys.argv.index(px)
        sys.argv.pop(idx) # remove option
        STATION_N = sys.argv[idx]
        sys.argv.pop(idx) # remove value
############################################
layout = dict(
    title='Time series with range slider and selectors',
    xaxis=dict(
        # rangeselector=dict(
        #     buttons=list([
        #         dict(count=10,
        #             label='10s',
        #             step = 'second',
        #             stepmode ='backward'),
        #         dict(count=100,
        #             step = 'second',
        #             label='100s',
        #             stepmode='backward'),
        #         dict(count=10,
        #             step = 'minute',
        #             label='10m',
        #             stepmode='todate'),
        #         dict(count=20,
        #             step = 'minute',
        #             label='20m',
        #             stepmode='backward'),
        #         dict(step='all')
        #     ])
        # ),
        # rangeslider=dict(),
        # type='seconds'
    ),
    yaxis=dict(
        # autorange=False,
        # showgrid=False,
        # zeroline=False,
        # showline=False,
        # autotick=True,
        # ticks='',
        # showticklabels=False
    )
)
#---------------------------------------------------------------------------------------

def plot_line(dType,M,B,Xf):
    X = []
    Y = []
    for x in range(len(scriptSys.data)) :
        X.append(int(scriptSys.data[x]['TIME']))
        Y.append(int(scriptSys.data[x][dType]))

    trace = go.Scatter(x = X,y = Y,mode = 'lines')
    y1 = []
    for x in range(0,Xf):
        y1.append(x * M + (B-Xf*M) )
    trace1 = go.Scatter(x = X,y = y1,mode = 'lines')

    # listax  = listax[0:200]
    y1a = [a * 1.1 for a in y1]
    # y1a = y1a[0:200]
    y1b = ([a * 0.9 for a in y1])
    # y1b = y1b[0:200]
    y1c = y1a + y1b[::-1]
    x1 = X + X[::-1]
    trace2 = go.Scatter(
    x = x1,
    y = y1c,
    fill='tozerox',
    fillcolor='rgba(0,100,80,0.2)',
    line=dict(color='transparent'),
    showlegend=True,
    name='Fair1',
    mode = 'lines'
    )
    data = [trace , trace1 ]
    plotly.offline.plot({"data": data,"layout": layout})
    return

#---------------------------------------------------------------------------------------

def plot_line1():
    data1 = [dict(
            visible = True,
            line=dict(color='00CED1', width=6),
            name = 'v = '+str(step),
            x = np.arange(0,100,0.01),
            y = np.sin(step*np.arange(0,10,0.01))) for step in np.arange(0,1,0.1)]
# data[10]['visible'] = True

 #---------------------------------------------------------------------------------------
	#abro la curva a evaluar
    try:
        with open("data/st"+STATION_N+".csv",'rb') as f:
            f.readline()
            f.readline()
            reader = csv.DictReader(f, delimiter=',')
            header = reader.fieldnames
            listax = []
            listay = []
            listay1 = []
            i=0
            for row in reader:
                listax.append(row["TIME"])
                listay.append(row["CURRENT"])
                i = i +1
                listay1.append(i*2+400)
            trace = go.Scatter(
            x = listax,
            y = listay,
            mode = 'lines'
            )
            trace1 = go.Scatter(
            x = listax[0:200],
            y = listay1,
            mode = 'lines'
            )

            listax  = listax[0:200]
            y1a = [a * 1.1 for a in listay1]
            y1a = y1a[0:200]
            y1b = ([a * 0.9 for a in listay1])
            y1b = y1b[0:200]
            y1c = y1a + y1b[::-1]
            x1 = listax + listax[::-1]
            trace2 = go.Scatter(
            x = x1,
            y = y1c,
            fill='tozerox',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='transparent'),
            showlegend=True,
            name='Fair1',
            mode = 'lines'
            )
            # amps_evaluar_aux=map(operator.itemgetter(2),file_evaluar)
            # amps_evaluar= [x for x in amps_evaluar_aux if x.isdigit()] #limpio la lista de los elementos no numericos
            # amps_evaluar=map(int,amps_evaluar)
        pass
    except:
        print "error con el csv"
        sys.exit()
        pass

    ############################################
    #     listax2 = []
    #     listay2 = []
    # for x in xrange(1000,2000):
    #     listax2.append(row["TIME"][x])
    #     listay2.append(row["CURRENT"][x])
    # trace2= go.Scatter(
    # x = listax2,
    # y = listay2,
    # mode = 'lines'
    # )



    data = [trace,trace1, trace2]
    plotly.offline.plot({"data": data,"layout": layout})
    return
