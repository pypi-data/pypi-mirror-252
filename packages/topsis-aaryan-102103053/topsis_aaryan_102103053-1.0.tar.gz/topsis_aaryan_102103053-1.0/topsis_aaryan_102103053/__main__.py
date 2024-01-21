from 102103053 import topsis,input_check
import sys
def main():
    input_check(5)
    inputFile, weights, impacts, resultFile = sys.argv[1:5]
    topsis(inputFile, weights, impacts, resultFile)
if __name__ == '__main__':
    main()