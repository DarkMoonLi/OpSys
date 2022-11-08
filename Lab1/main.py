import pandas as pd
import sys


def mealy_to_moore(dataframe):
    input_characters = []
    for item in dataframe['Unnamed: 0']:
        input_characters.append(item)

    data = df.drop('Unnamed: 0', axis=1)
    unique_states = []
    for rowIndex, row in data.iterrows():
        for columnIndex, value in row.items():
            if value not in unique_states:
                unique_states.append(value)

    letter = 'q'
    new_states = []
    finish_states = []
    index = 0
    for item in unique_states:
        new_states.append(letter + str(index))
        finish_states.append(item.split('/'))
        index += 1

    y = ['']
    for item in finish_states:
        y.append(item[1])

    finish = []
    array = [new_states]
    for index in range(0, len(input_characters)):
        finish.append(input_characters[index])
        for i in range(0, len(new_states)):
            column = dataframe[finish_states[i][0]]
            ind = unique_states.index(column[index])
            finish.append(new_states[ind])
        array.append(finish)
        finish = []
    array[0].insert(0, '')

    return pd.DataFrame(array, columns=[y])


def moore_to_mealy(dataframe):
    data = pd.DataFrame()
    columns = []

    for col in dataframe.columns:
        col = str(col).replace("'", "", 2)
        col = str(col).replace("(", "")
        col = str(col).replace(")", "")
        col = str(col).replace(",", "")
        col = col.split('.')[0]
        columns.append(col)

    for i in range(0, len(dataframe.index)):
        for j in range(0, len(columns)):
            if i != 0 and j != 0:
                data.at[i, j] = dataframe.iat[i, j] + '/' + columns[j]
            else:
                data.at[i, j] = dataframe.iat[i, j]

    column_names = data.iloc[0]
    data.drop(0, axis=0, inplace=True)
    data.columns = column_names
    return data


type_change = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]


df = pd.read_csv(input_file, delimiter=';')
result = pd.DataFrame()

if type_change == "mealy-to-moore":
    result = mealy_to_moore(df)

if type_change == "moore-to-mealy":
    result = moore_to_mealy(df)

f2 = open(output_file, 'w')
result.to_csv(f2, sep=';', index=False)
