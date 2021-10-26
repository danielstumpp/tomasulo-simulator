""" parser functions to convert input configurations into runnable simulator input"""
from simulator.modules.state import State
import yaml


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

    return True
        


def init_memory(state: State, mem_file: str):
    """ Initializes the memory of the state based on the provided memory file"""
    pass


def init_registers(state: State, reg_file: str):
    """ Initializes the registers of the state based on provided register value file"""
    pass


def parse_instructions(state: State, asm_file: str):
    """ Parses the input assembly file and adds instructions to the state"""
    pass
