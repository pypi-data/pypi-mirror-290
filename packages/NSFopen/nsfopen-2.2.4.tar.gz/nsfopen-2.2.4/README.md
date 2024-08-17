# NSFopen
Open Nanosurf NID files in Python

## Installing
From source
```
python setup.py install
```
or from PyPi
```
pip install nanosurf
```

## Prequisites
numpy
pandas
h5py

## Example Script
Available in example folder

### Example: NID File
```
from NSFopen.read import read
afm = nid_read('filename.nid')
data = afm.data # raw data
param = afm.param # parameters
```
