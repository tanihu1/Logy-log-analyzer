from ConfigParser import ConfigParser
import argparse

def main():
    parser = argparse.ArgumentParser(description="Logy - A log analyzer FOR the people, BY the people!")
    parser.add_argument('-l','--log-dir',type=str,required=True,help='Path to directory containing logs')
    parser.add_argument('-e','--events-file',type=str,required=True,help='Path to configuration file')
    parser.add_argument('-f','--from',type=str,required=False,help='Filter logs based on start timestamp')
    parser.add_argument('-t','--to',type=str,required=False,help='Filter logs based on end timestamp')
    args = parser.parse_args()
    print(args.log_dir)

if __name__ == "__main__":
    main()