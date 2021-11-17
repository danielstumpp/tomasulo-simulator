import argparse
from simulator import simulator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file')
    args = parser.parse_args()
    config_file = args.config_file

    state = simulator.run(config_file)

if __name__ == '__main__':
    main()
