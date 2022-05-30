import csv
import sys
import numpy as np

def cal_acc():
    pred, actual = [], []
    with open("test_predictions.csv", 'r') as rf:
                csvreader = csv.reader(rf)
                for row in csvreader:
                    data = int(row[0])
                    pred.append(data)
    with open("test_label.csv", 'r') as rf:
                csvreader = csv.reader(rf)
                for row in csvreader:
                    data = int(row[0])
                    actual.append(data)

    if len(actual) == len(pred):
        print(True)
    acc = 0
    for i in range(len(pred)):
        if pred[i] == actual[i]:
            acc += 1
    print(acc/len(pred) * 100.0)

if __name__ == "__main__":
    # print(sys.argv)
    cal_acc()
