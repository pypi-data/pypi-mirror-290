# AEMO NMI Lookup

## Introduction

The Australian Energy Market Operator (AEMO) is responsible for operating the National Electricity Market (NEM) and the Wholesale Electricity Market (WEM) in Western Australia. AEMO assigns a unique identifier to each electricity metering installation in the NEM and WEM, known as the National Meter Identifier (NMI). The NMI is a 10-character alphanumeric code that is used to identify the location of the metering installation.

## Installation

```bash
pip install aemo-nmi-lookup
```

## Usage

```python
from aemo_nmi_lookup import nmi_lookup

nmi = '8001234567'
state, participant_id = nmi_lookup(nmi)

print(f'State: {state}')
print(f'Participant ID: {participant_id}')
```

# License
MIT (c) 2024 Ian Connor

# Author
[Ian Connor](https://github.com/iconnor)


