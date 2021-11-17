
# tomasulo-simulator
[![Actions Status](https://github.com/danielstumpp/tomasulo-simulator/workflows/simulator/badge.svg)](https://github.com/danielstumpp/tomasulo-simulator/actions)

**View The most recent test report [here](https://htmlpreview.github.io/?https://github.com/danielstumpp/tomasulo-simulator/blob/main/test_report/test_report.html)**
---

Implementation of Tomasulo's Algorithm for CA

## Simulator Configuration
the simulator is configured using yaml configuration files with the following format:

```yaml
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

### Memory configuration

The memory configuration files are in csv format with the `.mem` extention. Below is the format where N is the number of non zero memory addresses after initialization. No need to specify memory locations to be set to zero. If multiple initializations of the same byte address occur then the latest one will be used.

```csv
<memory-byte-address-0>, <word-value>
        ...            ,    ...
        ...            ,    ...
        ...            ,    ...
<memory-byte-address-N>, <word_value>
```

### Register Configuration
The register configuration files use the same csv formatting, but with the `.reg` extension. If a float is added to an integer reg an error will be generated. The content is similar to memory configuration, accept with a string indicating the register. An example is below:

```csv
R1, 10
R2, 20
F2, 30.1
```

### Instruction Input
Instructions are provide in a `.asm` file and use the same format outlined in [here](doc/P1-description.pdf) with the exception that a comma is added between the operation and the first operand to allow easier parsing. An example is shown below:

```csv
Add.d, F1, F2, F3
Ld, F4, 8(R10)
Bne, R2, R3, -3
```

All instructions are validated before simulation begins and an error message indicating the line in error will be provided if issues are detected.

## Testing
Testing is automatically performed for pushes to the main branch or for pull requests. Pytest can be run locally by running `py.test` in the command line.