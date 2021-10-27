""" parser functions to convert input configurations into runnable simulator input"""
from os import read
from simulator.modules.state import State
import yaml
import csv


def load_config(state: State, config_file: str):
    """ Loads the specified yaml configuration file and returns loaded initial state by ref"""
    # open yaml file
    try:
        yaml_file = open(config_file)
    except:
        print("ERROR: config file -- " +config_file + " -- could not be opened!")
        return False

    try:
        config = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        print("Error in configuration file:", exc)
        return False

    # TODO

    return True
        


def init_memory(state: State, mem_file: str):
    """ Initializes the memory of the state based on the provided memory file"""
    # read in memory file as csv
    try:
        csv_file = open(mem_file,newline='')
    except:
        print("ERROR: memory file -- " +
              mem_file + " -- could not be opened!")
        return False

    try:
        reader = csv.reader(csv_file,delimiter=',')
    except:
        print("ERROR: could not read mem file")
        return False

    reader_list = list(reader)
    for i in range(len(reader_list)):
        line = reader_list[i]

        # ensure inputs are numeric
        try:
            float(line[0].strip())
            float(line[1].strip())
        except:
            print("ERROR: Non-numeric memory entry -> line ", i + 1)
            return False

        addr = int(line[0].strip())
        val = float(line[1].strip())

        if addr < 256 and addr >= 0 and addr % 4 == 0:
            state.memory[int(addr/4)] = val
        else:
            print("ERROR: Invalid memory entry -> line ",i + 1)
            return False

    return True



def init_registers(state: State, reg_file: str):
    """ Initializes the registers of the state based on provided register value file"""
    pass


def parse_instructions(state: State, asm_file: str):
    """ Parses the input assembly file and adds instructions to the state"""
    pass


