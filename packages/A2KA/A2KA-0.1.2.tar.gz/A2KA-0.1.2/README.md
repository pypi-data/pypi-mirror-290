# A2KA
A2KA is a novel web architecture designed to
identify crucial areas by extracting biological information from the embedding space of large language models.
Make sure pytorch is installed firstly.
The github storage is: https://github.com/Dsadd4/NLSExplorer_1.0
## Installation

You can install A2KA via pip:

```bash
pip install A2KA
```
## Usage
A2KA
```python
from A2KA import A2KA
import torch
hidden_dimention = 512
#configure your A2KA sturcture
config = [8,8,32]
#If your datasize is significant large, extending the scale of the network may be a good choice.
#Such a config = 18*[64] means it has 18 layers and each layer has 64 basic attention units.
model =A2KA( hidden_dimention,config)
# tensor in a shape of (Batchsize,sequence_length, embedding dimension)
exampletensor = torch.randn(5,100,512)
prediction,layerattention = model(exampletensor)
print(prediction)
print(layerattention)
```
SCNLS (in linux system)
```python
from A2KA import SCNLS
#Example 
sequence_for_analysis = ['MSSAKRRKK','LSSSSKVR','MTNLP']
kth_set = 3
max_gap = 3
processorsnumber = 2
result = SCNLS(sequence_for_analysis,kth_set,max_gap,processorsnumber):
```
