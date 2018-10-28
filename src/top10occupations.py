import os
import csv
import sys

def main(argv):
    csv.field_size_limit(100000000)
    input_file = argv[0]
    result_data = []
    with open(input_file, 'r', errors='ignore') as csvfile:
        input_data = csv.reader(csvfile)
        for row in input_data:
            temp = "".join(row).split(';')
            result_data.append(temp)
    col_header = result_data[0]
    row_data = result_data[1:]

    # Column numbers to group data on.
    if 'CASE_STATUS' in col_header:
        status = col_header.index('CASE_STATUS')
    elif 'STATUS' in col_header:
        status = col_header.index('STATUS')
    else:
        print("error message")

    if 'SOC_NAME' in col_header:
        occupation = col_header.index('SOC_NAME')
    elif 'LCA_CASE_SOC_NAME' in col_header:
        occupation = col_header.index('LCA_CASE_SOC_NAME')
    else:
        print("error message")

    if 'WORKSITE_STATE' in col_header:
        work_state = col_header.index('WORKSITE_STATE')
    elif 'LCA_CASE_EMPLOYER_STATE' in col_header:
        work_state = col_header.index('LCA_CASE_EMPLOYER_STATE')
    else:
        print("error message")

    top_10_occupations = top10info(status, occupation, row_data)
    top_10_states = top10info(status, work_state, row_data)

    with open('top_10_occupations.txt', 'w') as f:
        f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
        for occupations in top_10_occupations:
            f.write(','.join(str(v) for v in occupations)+"\n")
        f.close()

    with open('top_10_states.txt', 'w') as f:
        f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
        for states in top_10_states:
            f.write(','.join(str(v) for v in states)+"\n")
        f.close()

def top10info(status, group_by_column, row_data):
    """ Returns the top 10 results grouped by :param group_by_column. Sorts alphabetically if there is a tie. """

    confirmed_cases = []
    for row in row_data:
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
        top10_info.append([i[1].replace('"',''), i[0], str(i[2])+"%"])
    top10_info.sort(key=lambda row: row[0])
    top10_info.sort(key=lambda row: row[1], reverse=True)
    return (top10_info)


if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 3:
        print("Usage: " + os.path.basename(__file__) + " <input_file> <top10occupations_file> <top10companies_file>")
        sys.exit(1)

    main(args)
