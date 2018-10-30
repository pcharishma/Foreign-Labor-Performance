import os
import csv
import sys

def main():

    # To accommodate large field sizes
    csv.field_size_limit(10000000)
    basepath = '/input/'

    input_file_name = os.listdir(os.getcwd() + basepath )[0]
    certified_occupations = []
    certified_states=[]
    with open(os.getcwd() + basepath + input_file_name, 'rbU') as csvfile:
        input_data = csv.reader(csvfile, delimiter=';')

        for row in input_data:
            header = row
            break

        # Column numbers to group data on.
        if ('CASE_STATUS' in header) and ('SOC_NAME' in header) and ('WORKSITE_STATE' in header):
            status = header.index('CASE_STATUS')
            occupation = header.index('SOC_NAME')
            work_state = header.index('WORKSITE_STATE')

            for row in input_data:
                if row[status]=='CERTIFIED':
                    certified_occupations.append(row[occupation])
                    certified_states.append(row[work_state])


        elif ('STATUS' in header) and ('LCA_CASE_SOC_NAME' in header) and ('LCA_CASE_EMPLOYER_STATE' in header):
            status = header.index('STATUS')
            occupation = header.index('LCA_CASE_SOC_NAME')
            work_state = header.index('LCA_CASE_EMPLOYER_STATE')
            for row in input_data:
                if row[status]=='CERTIFIED':
                    certified_occupations.append(row[occupation])
                    certified_states.append(row[work_state])

        else:
            print("Input format incorrect. Please check the data format.")
            exit(2)


    top_10_occupations = top10data(certified_occupations)
    top_10_states = top10data(certified_states)

    with open(os.getcwd() + '/output/top_10_occupations.txt', 'w') as f:
        f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+"\n")
        for occupations in top_10_occupations:
            f.write(';'.join(str(v) for v in occupations)+"\n")
        f.close()

    with open(os.getcwd() + '/output/top_10_states.txt', 'w') as f:
        f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+"\n")
        for states in top_10_states:
            f.write(';'.join(str(v) for v in states)+"\n")
        f.close()

def top10data(row_data):
    """ Returns the top 10 results by counts. Sorts alphabetically if there is a tie. """

    aggregate_counts = {}
    for t in row_data:
        if t not in aggregate_counts:
            aggregate_counts[t] = 1
        else:
            aggregate_counts[t] += 1

    total_certified = len(row_data)

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