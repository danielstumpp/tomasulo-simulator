import argparse
from simulator import simulator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file')
    args = parser.parse_args()
    config_file = args.config_file

    state = simulator.run(config_file)
    
    tt = simulator.TimingTable()
    tt.load_from_state(state)
    print(tt)
    print('\nREGISTER VALUES: \n' + state.get_register_table())
    print('\nNON-ZERO MEMORY VALUES: \n' + state.get_non_zero_memory_table())

if __name__ == '__main__':
    main()
