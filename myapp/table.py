import pandas as pd
from prettytable import PrettyTable
def send(csv_file):

    data_set=pd.read_csv(csv_file)
    return data_set.values.tolist()
