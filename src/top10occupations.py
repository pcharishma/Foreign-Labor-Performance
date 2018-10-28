import os
import csv
import sys
import regex as re


def main(argv):
    input_file = argv[0]
    print(input_file)
    result_data = []
    with open(input_file,'r') as csvfile:
        input_data = csv.reader(csvfile)
        for row in input_data:
            temp = [', '.join(row)][0].split(';')
            #temp1 = re.split(r'\n[0-9]',temp)
            #print(temp1)
            result_data.append(temp)

    col_header = result_data[0]
    row_data = result_data[1:]

    # Column numbers to group data on.
    status = col_header.index('CASE_STATUS')
    occupation = col_header.index('SOC_NAME')
    work_state = col_header.index('WORKSITE_STATE')

    top_10_occupations = top10info(status, occupation, row_data)
    top_10_states = top10info(status, work_state, row_data)

    print(top_10_occupations)
    print(top_10_states)


def top10info(status, group_by_column, row_data):
    """ Returns the top 10 results grouped by :param group_by_column. Sorts alphabetically if there is a tie. """

    confirmed_cases = []
    for row in row_data:
        print(row)
        if row[status] == "CERTIFIED":
            confirmed_cases.append([row[status], row[group_by_column]])

    aggregate_counts = {}
    for t in confirmed_cases:
        if t[1] not in aggregate_counts:
            aggregate_counts[t[1]] = 1
        else:
            aggregate_counts[t[1]] += 1

    total_certified = len(confirmed_cases)

    percents = []
    for title, counts in aggregate_counts.items():
        percents.append([counts, title, round(float(counts / total_certified) * 100, 2)])
    percents.sort(reverse=True)

    num = min(len(percents),10)
    top10 = percents[:num]
    top10_info = []
    for i in top10:
        top10_info.append([i[1], i[0], i[2]])

    return (top10_info)


if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 3:
        print("Usage: " + os.path.basename(__file__) + " <input_file> <top10occupations_file> <top10companies_file>")
        sys.exit(1)

    main(args)
