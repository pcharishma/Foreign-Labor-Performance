import os
import csv
import sys

def main():

    maxInt = sys.maxsize;
    decrement = True;

    # To accomodate long fields.
    while decrement:
        decrement= False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
    basepath = '\\input\\'

    input_file = os.listdir(os.getcwd() + basepath )[0]
    result_data = []
    with open(os.getcwd() + basepath + input_file, 'r',errors='ignore') as csvfile:
        input_data = csv.reader(csvfile)
        for row in input_data:
            temp = "".join(row).split(';')
            result_data.append(temp)
    col_header = result_data[0]
    row_data = result_data[1:]

    # Column numbers to group data on.
    if ('CASE_STATUS' in col_header)&('SOC_NAME' in col_header)&('WORKSITE_STATE' in col_header):
        status = col_header.index('CASE_STATUS')
        occupation = col_header.index('SOC_NAME')
        work_state = col_header.index('WORKSITE_STATE')
    elif ('STATUS' in col_header)&('LCA_CASE_SOC_NAME' in col_header)&('LCA_CASE_EMPLOYER_STATE' in col_header):
        status = col_header.index('STATUS')
        occupation = col_header.index('LCA_CASE_SOC_NAME')
        work_state = col_header.index('LCA_CASE_EMPLOYER_STATE')
    else:
        print("error message")

    top_10_occupations = top10info(status, occupation, row_data)
    top_10_states = top10info(status, work_state, row_data)

    with open(os.getcwd() + '\\output\\top_10_occupations.txt', 'w') as f:
        f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+"\n")
        for occupations in top_10_occupations:
            f.write(';'.join(str(v) for v in occupations)+"\n")
        f.close()

    with open(os.getcwd() + '\\output\\top_10_states.txt', 'w') as f:
        f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+"\n")
        for states in top_10_states:
            f.write(';'.join(str(v) for v in states)+"\n")
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
        percents.append([counts, title])
    percents.sort(reverse=True)

    num = min(len(percents),10)
    top10 = percents[:num]

    top10_info = []
    for i in top10:
        top10_info.append([i[1].replace('"',''), i[0], str(round((float(i[0]) / total_certified) * 100, 2))+"%"])
    top10_info.sort(key=lambda row: row[0])
    top10_info.sort(key=lambda row: row[1], reverse=True)
    return (top10_info)


if __name__ == "__main__":
    main()
