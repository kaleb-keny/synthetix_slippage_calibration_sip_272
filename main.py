#!/usr/bin/env python3
from utils.charting import Chart
import argparse

if __name__ == '__main__':
    description = \
    '''
    Please enter the exponents of the model (typically, [0,0.5,1,2])
    
        python main.py -e 0 0.5 1 2

    '''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-e",
                        type=float,
                        nargs='+',
                        required=False)

    args = parser.parse_args()
    
    if args.e:
        exponentList = args.e
    else:
        exponentList = [0.5,1]
    
    chart = Chart(exponentList=exponentList)
    chart.chart_data()
    print("Modelling successful and outputs updated!")
