
## Install : 
```bash 
pip install PyDefold
```

## Example : 
```python
from PyDefold import Defold  , version
from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import MessageToString , Parse 

print(f'defoldsdk version = {version}')
collection = Defold.CollectionDesc()
print(MessageToString(collection))
```