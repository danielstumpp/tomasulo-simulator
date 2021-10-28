
# tomasulo-simulator
[![Actions Status](https://github.com/danielstumpp/tomasulo-simulator/workflows/simulator/badge.svg)](https://github.com/danielstumpp/tomasulo-simulator/actions)

Implementation of Tomasulo's Algorithm for CA

## Simulator Configuration
the simulator is configured using yaml configuration files with the following format:

```
# yaml name field
name: test1_config

# Functional Unit Resources
FUs:
  # integer adders
  IA: 
    numRS: 2
    exCycles: 1
    memCycles: 0
    instances: 1
  FPA:
    numRS: 3
    exCycles: 3
    memCycles: 0
    instances: 1
  FPM:
    numRS: 2
    exCycles: 20
    memCycles: 0
    instances: 1
  LSU:
    numRS: 2
    exCycles: 20
    memCycles: 0
    instances: 1

ROBentries: 128
CDBbufferLength: 1

# init files
memInitFile: path/from/root/memfile.mem
regInitFile: path/from/root/regfile.reg
instFile: path/from/root/instfile.asm
```

All fields are required except for the `memInitFile` and `regInitFile` fields. If those are not included all registers and memory will be initialized to zero. Paths are represented as the relative path from the root directory of the repository.

## Testing
Testing is automatically performed for pushes to the main branch or for pull requests. Pytest can be run locally by running `py.test` in the command line.