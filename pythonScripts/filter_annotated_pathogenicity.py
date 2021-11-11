import pandas as pd


def open_tsv(location):
    return pd.read_csv(location, sep="\t")


def filter_data(data):
    return data[((data.CLNREVSTAT == "reviewed by expert panel") |
                (data.CLNREVSTAT == "practice guideline")) &
                (data.CLNSIG != "Uncertain significance")]


def write_tsv(data):
    data.to_csv("ML data.tsv", sep="\t", index=False)


if __name__ == '__main__':
    subset = filter_data(open_tsv("results_new.tsv"))
    write_tsv(subset)
