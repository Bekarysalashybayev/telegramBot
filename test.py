import csv


def getRow(value):
    data = ''
    with open('BankChurners.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == value:
                data = f'ID: {row[0]} \n ' \
                                     f'Attrition_Flag: {row[1]} \n' \
                                     f'Customer_Age: {row[2]} \n' \
                                     f'Gender: {row[3]} \n' \
                                     f'Dependent_count: {row[4]} \n' \
                                     f'Education_Level: {row[5]} \n' \
                                     f'Marital_Status: {row[6]} \n' \
                                     f'Income_Category: {row[7]} \n' \
                                     f'Card_Category: {row[8]} \n' \
                                     f'Months_on_book: {row[9]} \n' \
                                     f'Total_Relationship_Count: {row[10]} \n' \
                                     f'Months_Inactive_12_mon: {row[11]} \n' \
                                     f'Contacts_Count_12: {row[12]} \n'

    return data


# val = getRow('718372458')
# print(val)
