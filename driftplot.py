import numpy as np
import glob
import gzip
import os
from astropy.io import fits
from astropy.table import Table
from matplotlib import pyplot as plt
#-------------------------------------------------------------------------------

def get_osmT(files):
    dat= open(files)
    print dat.name[-12:]
    data= dat.readlines()
    block= []
    for line in data:
        line= line[0:131]
        line= line.split()
        if not line:
            continue
        elif line[0] == 'COS' or line[0] == 'Data' or line[0] == 'Filename':
            continue
        elif line[0][0] == '-':
            continue
        else:
            block.append(line)

    rootname= []
    T_OSM1= []
    T_OSM2= []
    OSM1= []
    OSM2= []
    prop= []

    for row in block:
        if 'NCM1'in row or 'MIRRORA' in row or 'MIRRORB' in row or\
            'NCM1FLAT' in row:
            continue
        t1= row[-2]
        t2= row[-1]
        try:
            t1, t2= float(t1), float(t2)
        except ValueError:
            continue
        T_OSM1.append(t1)
        T_OSM2.append(t2)
        OSM1.append(row[-6])
        OSM2.append(row[-5])
        rootname.append(row[0])
        prop.append(row[1])

    T= Table([rootname, prop, T_OSM1, T_OSM2, OSM1, OSM2], names= ('rootnames',
             'Prop ID', 'T1', 'T2', 'OSM1', 'OSM2'))
    #T.write('{}_dat.txt'.format(dat.name[:-4]), format= 'ascii.tab')
    dat.close

    return T

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    dr= '/user/jwhite/reports/'
    plt.figure()
# look at turning this one figure into a subplot figure so that you can look at
# displacement as well as drift values in the same figure
    for files in glob.glob(dr + '*.txt'):
        table= get_osmT(files)
        rootnames= np.array(table['rootnames'])
        propID= np.array(table['Prop ID'])
        T1= np.array(table['T1'])
        for p in rootnames:
            for dirpath, dirnames, filenames in os.walk(
            '/smov/cos/Data/{}/otfrdata/'.format(propID[np.where(rootnames == p)[0][0]]
            ),topdown= True):
                for name in filenames:
                    if name[-18:] == '_lampflash.fits.gz':
                        print os.path.join(dirpath, name)
                        lamp_file= os.path.join(dirpath, name)
                        lamp_dat= Table.read(lamp_file)
                        lamp_shifts= -1* np.array(lamp_dat['SHIFT_DISP'])
                        plt.plot(np.ones(len(lamp_shifts))* T1[np.where(
                               rootnames == p)[0][0]], lamp_shifts, 'ro')
                    else:
                        continue


    plt.show()
