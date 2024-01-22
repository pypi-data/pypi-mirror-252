import endf6
import numpy as np
import pandas as pd 
import random

df = pd.DataFrame.from_dict({
    'energy': np.linspace(1e-5, 20e6, 100),
    })
df['xs'] = 1 / df['energy']

int_ranges = np.random.randint(1, len(df), 3)  
int_ranges = np.unique(np.sort(int_ranges))
int_ranges = np.concatenate([int_ranges, [len(df)]])
int_laws = np.random.randint(1, 5, len(int_ranges)) 
int_lens = np.concatenate([int_ranges[0:1], np.diff(int_ranges)])
# for fortran routine
df['int'] = np.concatenate([np.full(s, l) for s, l in zip(int_lens, int_laws)])

# quantities to provide to reactions
MAT = 2625
MF = 3
MT = 1
AWR = 56.
Z = 26
A = 56
QM = 0.
ELIS = 0
Ex = 0
LR = 1

ZA = float(Z*1000 + A)
QI = float(QM + ELIS - Ex)

jou = 0

NR = len(df) - 1
NP = len(df)

nou = np.empty((80,10000), dtype='S1', order='C')

nou, jou = endf6.endf6.wrtmf3mt_ext(nou, jou, MAT, MF, MT, ZA, AWR, QM, QI, LR, NR, df['int'], NP, df['energy'], df['xs'])  

tmp = np.apply_along_axis(lambda p: bytes(p), 0, nou[:,:jou])
tmp = [p.decode() for p in tmp.tolist()]
tmp
print('\n'.join(tmp))

nou, jou = endf6.endf6.wrtmf3mt_lin(nou, jou, MAT, MF, MT, ZA, AWR, QM, QI, LR, NP, df['energy'], df['xs'])

jin=0
nbt = np.empty(20, dtype=int)
ibt = np.empty(20, dtype=int)
x = np.empty(10000, dtype=float)
y = np.empty(10000, dtype=float)

nou2,jin,za,awr,qm,qi,lr,nr,nbt,ibt,np,x,y = endf6.endf6.readmf3mt_std(nou, jin, nbt, ibt, x, y)










 
textstr = np.array('hallo', np.dtype('S66'))
textstr2 = np.array('pfau', np.dtype('S66'))
textstr3 = np.array('huhei', np.dtype('S66'))

xstr = np.empty((80,10), dtype='S1', order='C')
xstrout = endf6.endf6.wrtext(xstr, 0, 2100, 3, 1, 500, textstr) 
xstrout = endf6.endf6.wrtext(xstrout, 1, 2100, 3, 1, 500, textstr2) 

tmp = np.apply_along_axis(lambda p: bytes(p), 0, xstrout[:,:2])
tmp = [p.decode() for p in tmp.tolist()]
