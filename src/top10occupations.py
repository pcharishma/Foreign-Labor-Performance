import xlrd
ExcelFileName='H-1B_Disclosure_Data_FY15_Q4.xlsx'
workbook = xlrd.open_workbook(ExcelFileName)
worksheet = workbook.sheet_by_name("H-1B_FY2015") # We need to read the data
#from the Excel sheet named "H-1B_FY2016"
num_rows = worksheet.nrows #Number of Rows
num_cols = worksheet.ncols #Number of Columns
result_data =[]
for curr_row in range(0, num_rows, 1):
    row_data = []
    for curr_col in range(0, num_cols, 1):
        data = worksheet.cell_value(curr_row, curr_col) # Read the data in the current cell
        row_data.append(data)
    result_data.append(row_data)
col_header = result_data[0]
row_data = result_data[1:]

# we are getting the column numbers for the required data
status = col_header.index("CASE_STATUS")
occupation = col_header.index("SOC_NAME")
work_state = col_header.index("WORKSITE_STATE")

def top10_occupations(status,occupation,row_data):
    certified_casesby_occupation = []
    for row in row_data:
        if row[status] =="CERTIFIED":
            certified_casesby_occupation.append([row[status],row[occupation]])
    
    occupation_counts={}
    for t in certified_casesby_occupation:
        if t[1] not in occupation_counts:
            occupation_counts[t[1]] = 1
        else:
            occupation_counts[t[1]]+=1
    
    total_certified = len(certified_casesby_occupation)
    
    occupation_counts_percent = []
    for title,counts in occupation_counts.items():
        occupation_counts_percent.append([counts,title,round(float(counts/total_certified)*100,2)])
    occupation_counts_percent.sort(reverse =True)
    
    top10 = occupation_counts_percent[:10]
    top10_occupations = []
    for i in top10:
        top10_occupations.append([i[1],i[0],i[2]])
    
    return(top10_occupations)
	
def top_10_workStates(status,work_state,row_data):
    certified_casesby_state = []
    for row in row_data:
        if row[status] =="CERTIFIED":
            certified_casesby_state.append([row[status],row[work_state]])
    
    workState_counts={}
    for t in certified_casesby_state:
        if t[1] not in workState_counts:
            workState_counts[t[1]] = 1
        else:
            workState_counts[t[1]]+=1
    
    total_certified = len(certified_casesby_state)
    
    state_counts_percent = []
    for state,counts in workState_counts.items():
        state_counts_percent.append([counts,state,round(float(counts/total_certified)*100,2)])
    state_counts_percent.sort(reverse =True)
    
    top10 = state_counts_percent[:10]
    top10_states = []
    for i in top10:
        top10_states.append([i[1],i[0],i[2]])
    
    return(top10_states)
	
top_10_occupations = top10_occupations(status,occupation,row_data)
top_10_states = top_10_workStates(status,work_state,row_data)

print(top_10_occupations)
print(top_10_states)