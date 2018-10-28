import os
import sys
import xlrd


def main(argv):
    input_file = argv[1]
    workbook = xlrd.open_workbook(input_file)
    worksheet = workbook.sheet_by_name("H-1B_FY2015")  # We need to read the data
    # from the Excel sheet named "H-1B_FY2016"
    num_rows = worksheet.nrows  # Number of Rows
    num_cols = worksheet.ncols  # Number of Columns
    result_data = []
    for curr_row in range(0, num_rows, 1):
        row_data = []
        for curr_col in range(0, num_cols, 1):
            data = worksheet.cell_value(curr_row, curr_col)  # Read the data in the current cell
            row_data.append(data)
        result_data.append(row_data)
    col_header = result_data[0]
    row_data = result_data[1:]

    # Column numbers to group data on.
    status = col_header.index("CASE_STATUS")
    occupation = col_header.index("SOC_NAME")
    work_state = col_header.index("WORKSITE_STATE")

    top_10_occupations = top10info(status, occupation, row_data)
    top_10_states = top10info(status, work_state, row_data)

    print(top_10_occupations)
    print(top_10_states)


def top10info(status, group_by_column, row_data):
    """ Returns the top 10 results grouped by :param group_by_column. Sorts alphabetically if there is a tie. """

    aggregate_cases = []
    for row in row_data:
        if row[status] == "CERTIFIED":
            aggregate_cases.append([row[status], row[group_by_column]])

    aggregate_counts = {}
    for t in aggregate_cases:
        if t[1] not in aggregate_counts:
            aggregate_counts[t[1]] = 1
        else:
            aggregate_counts[t[1]] += 1

    total_certified = len(aggregate_cases)

    percents = []
    for title, counts in aggregate_counts.items():
        percents.append([counts, title, round(float(counts / total_certified) * 100, 2)])
    percents.sort(reverse=True)

    top10 = percents[:10]
    top10_info = []
    for i in top10:
        top10_info.append([i[1], i[0], i[2]])

    return (top10_info)


if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 3:
        print "Usage: " + os.path.basename(__file__) + " <input_file> <top10occupations_file> <top10companies_file>"
        sys.exit(1)

    main(args)
