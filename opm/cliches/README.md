```
fh = open('/home/rik/Desktop/flush.txt', 'r')
raw_text = fh.read()
fh.close()
from cliches.cliche import main as cliche_check
from cliches.cliches import main as cliche_check
results = cliche_check(raw_text)
results[0]
print results[1]
```
