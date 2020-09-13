import matplotlib.pyplot as plt

def plt2pic(data_act):
    if data_act.empty==False:

        try:
            data_act.plot()
            plt.show()
        except:
            print(data_act)
