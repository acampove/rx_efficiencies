'''
Module storing data classes needed by tests
Also pytest functions intended to be run after tests
'''

import mplhep
import pandas            as pnd
import matplotlib.pyplot as plt
from rx_efficiencies.decay_names import DecayNames as dn

# -----------------------------------
class ScalesData:
    '''
    data class
    '''
    df = pnd.DataFrame(columns=['Process', 'Q2', 'Value', 'Error'])

    plt.style.use(mplhep.style.LHCb2)
    # ------------------
    @staticmethod
    def collect(proc : str, q2bin : str, value : float, error : float) -> None:
        '''
        Picks test outputs and uses it to fill dataframe
        '''
        size                    = len(ScalesData.df)
        ScalesData.df.loc[size] = [proc, q2bin, value, error]
    # ------------------
    @staticmethod
    def plot_scales():
        '''
        Plots scales from dataframe
        '''
        ax = None
        for proc, df_proc in ScalesData.df.groupby('Process'):
            decay = dn.tex_from_decay(proc)
            ax = df_proc.plot(x='Q2', y='Value', yerr='Error', label=decay, ax=ax, figsize=(13, 10))

        plt.xlabel('')
        plt.ylabel('$N_{signal}/N_{PRec}$')
        plt.savefig('scales.png')
        plt.close()
# -----------------------------------
def pytest_sessionfinish(session, exitstatus):
    '''
    Runs at the end
    '''
    ScalesData.plot_scales()
