# spinneroo

> A module for displaying progress messages and timers with spinners in the command line.

## Installation
```
pip install spinneration
```

## example
```python
import time

from spinneration import Spinner

spinner1 = Spinner(
    title='Process 1',
    message='processing',
    complete="complete",
    counter=True,
    clean=True,
    silence=False
)
spinner1.spin()

time.sleep(5)

spinner2 = Spinner(
    title='Process 2',
    message='processing',
    complete="complete",
    counter=True,
    clean=True,
    silence=False
)
spinner2.spin()

time.sleep(5)

spinner2.stop()

time.sleep(5)

spinner1.stop()
```

final output
```
Process 1: Paused 00:00:05       
Process 2: complete 00:00:05     
Process 1: complete 00:00:15
```