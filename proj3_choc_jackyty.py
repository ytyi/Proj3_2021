import sqlite3
import plotly.graph_objects as go
# unique name=jackyty

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'

# Part 1: Implement logic to process user commands
def process_command(command):
    sql_command = prase_list_process(get_prase_list(command))
    conn = sqlite3.connect('choc.sqlite')
    cur = conn.cursor()
    cur.execute(sql_command)
    results_arr = []
    for idx, row in enumerate(cur):
        row = list(row)
        col = []
        for i in range(len(row)):
            col.append(row[i])
        results_arr.append(tuple(col))
    return results_arr


def print_list(command, result):
    def filter(inp):
        oup = []
        for i, x in enumerate(inp):
            if type(x) == float:
                if i == 4:
                    oup.append(float("{:.2f}".format(x)))
                else:
                    oup.append("{:.1f}".format(x))
            else:
                if len(str(x)) > 12:
                    oup.append((x[0:12] + '...'))
                else:
                    oup.append(x)
        return oup

    if command.split()[0] == 'bars':
        style = "{:<16}{:<16}{:<16}{:<5}{:<5.0%}{:<16}".format
        for x in result:
            x = filter(x)
            print(style(x[0], x[1], x[2], x[3], x[4], x[5]))

    if command.split()[0] == 'companies' or command.split()[0] == 'countries':
        style = "{:<16}{:<16}{:<16}".format
        for x in result:
            x = filter(x)

            print(style(x[0], x[1], x[2]))

    if command.split()[0] == 'regions':
        style = "{:<16}{:<16}".format
        for x in result:
            x = filter(x)
            print(style(x[0], x[1]))



def get_prase_list(command):
    options_0 = ['bars', 'companies', 'countries', 'regions']
    options_1 = ['none', 'country', 'region']
    options_2 = ['sell', 'source']
    options_3 = ['ratings', 'cocoa', 'number_of_bars']
    options_4 = ['top', 'bottom']
    options = [options_0, options_1, options_2, options_3, options_4]
    prase_list = ['bars', 'sell', 'sell', 'ratings', 'top','10']
    for i in range(len(command.split())):
        x = command.split()[i].split('=')[0]
        x1 = command.split()[i]
        for index, j in enumerate(options):
            if x in j:
                prase_list[index] = x1

    '''
    while len(prase_list)<5:
        try:
            x=command.split()[i].split('=')[0]
            x1=command.split()[i]
        except:
            x=''
            x1=''
        if len(prase_list)==0:
            prase_list.append(x1)
            i=i+1
        elif len(prase_list)==1:
            if x in options_1:
                prase_list.append(x1)
                i=i+1
            else:
                prase_list.append('none')
        elif len(prase_list)==2:
            if  x in options_2:
                prase_list.append(x1)
                i=i+1
            else:
                prase_list.append('sell')
        elif len(prase_list)==3:
            if  x in options_3:
                prase_list.append(x1)
                i=i+1
            else:
                prase_list.append('ratings')
        elif len(prase_list)==4:
            if x in options_4:
                prase_list.append(x1)
                i=i+1
            else:
                prase_list.append('top')
    '''

    if command.split()[-1] == 'barplot':
        if command.split()[-2].isnumeric():
            prase_list[5] = (command.split()[-2])
        prase_list.append('barplot')
    else:
        if command.split()[-1].isnumeric():
            prase_list[5] = (command.split()[-1])
    return prase_list

def prase_list_process(prase_list):

    if prase_list[0] == 'bars':
        prase_dict = {'ratings': 'Rating', 'cocoa': 'CocoaPercent', 'top': 'DESC', 'bottom': 'ASC'}
        data_command = 'SELECT SpecificBeanBarName, Company, sell.EnglishName, Rating, CocoaPercent, source.EnglishName FROM Bars, Countries source, Countries sell WHERE '
        if prase_list[1].split('=')[0] == 'country':
            data_command = data_command + f"{prase_list[2]}.Alpha2='{prase_list[1].split('=')[1]}' AND "
        elif prase_list[1].split('=')[0] == 'region':
            data_command = data_command + f"{prase_list[2]}.Region='{prase_list[1].split('=')[1]}' AND "
        data_command = data_command + f'Bars.BroadBeanOriginId=source.Id AND Bars.CompanyLocationId=sell.Id ORDER BY {prase_dict[prase_list[3]]} {prase_dict[prase_list[4]]} LIMIT {prase_list[5]}'

    if prase_list[0] == 'companies':
        prase_dict = {'number_of_bars': 'COUNT(SpecificBeanBarName)', 'ratings': 'AVG(Rating)',
                      'cocoa': 'AVG(CocoaPercent)', 'top': 'DESC', 'bottom': 'ASC'}
        data_command = f'SELECT Company, EnglishName, {prase_dict[prase_list[3]]} FROM Bars JOIN Countries ON Bars.CompanyLocationId=Countries.Id '
        if prase_list[1].split('=')[0] == 'country':
            data_command = data_command + f"WHERE Alpha2='{prase_list[1].split('=')[1]}'"
        elif prase_list[1].split('=')[0] == 'region':
            data_command = data_command + f"WHERE Region='{prase_list[1].split('=')[1]}'"
        data_command = data_command + f' GROUP BY Company HAVING COUNT(SpecificBeanBarName) > 4 ORDER BY {prase_dict[prase_list[3]]} {prase_dict[prase_list[4]]} LIMIT {prase_list[5]}'

    if prase_list[0] == 'countries':

        prase_dict = {'number_of_bars': 'COUNT(SpecificBeanBarName)', 'ratings': 'AVG(Rating)',
                      'cocoa': 'AVG(CocoaPercent)', 'top': 'DESC', 'bottom': 'ASC'}
        data_command = f'SELECT EnglishName, Region, {prase_dict[prase_list[3]]} FROM Bars JOIN Countries '
        if prase_list[2] == 'source':
            data_command = data_command + 'ON Bars.BroadBeanOriginId=Countries.Id '
        else:
            data_command = data_command + 'ON Bars.CompanyLocationId=Countries.Id '

        if prase_list[1].split('=')[0] == 'region':
            data_command = data_command + f" WHERE Region='{prase_list[1].split('=')[1]}'"
        data_command = data_command + f'GROUP BY EnglishName HAVING COUNT(SpecificBeanBarName) > 4 ORDER BY {prase_dict[prase_list[3]]} {prase_dict[prase_list[4]]} LIMIT {prase_list[5]} '

    if prase_list[0] == 'regions':
        prase_dict = {'number_of_bars': 'COUNT(SpecificBeanBarName)', 'ratings': 'AVG(Rating)',
                      'cocoa': 'AVG(CocoaPercent)', 'top': 'DESC', 'bottom': 'ASC'}
        data_command = f"SELECT Region, {prase_dict[prase_list[3]]} FROM Bars JOIN Countries "
        if prase_list[2] == 'source':
            data_command = data_command + 'ON Bars.BroadBeanOriginId=Countries.Id '
        else:
            data_command = data_command + 'ON Bars.CompanyLocationId=Countries.Id '
        data_command = data_command + f'GROUP BY Region HAVING COUNT(SpecificBeanBarName) > 4 ORDER BY {prase_dict[prase_list[3]]} {prase_dict[prase_list[4]]} LIMIT {prase_list[5]}'

    return data_command

def load_help_text():
    with open('Proj3Help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    user_command = ''
    while user_command != 'exit':
        user_command = input('Enter a command: ')
        if user_command.strip() == '':
            print()
            continue
        if user_command == 'help':
            print(load_help_text())
            continue
        if user_command == 'exit':
            print('bye')
            break
        options_0 = ['bars', 'companies', 'countries', 'regions']
        options_1 = ['none', 'country', 'region']
        options_2 = ['sell', 'source']
        options_3 = ['ratings', 'cocoa', 'number_of_bars']
        options_4 = ['top', 'bottom']
        options = [options_0, options_1, options_2, options_3, options_4]
        correct_list = []
        i = -1
        flag = 1

        for x in user_command.split():
            for j in range(i + 1, len(options)):
                if x.split('=')[0] in options[j]:
                    i = j
                    correct_list.append(i)
                    break
        if not user_command.split()[-1] == 'barplot':
            if not user_command.split()[-1].isnumeric():
                if len(correct_list) != len(user_command.split()):
                    flag = 0
                    print('Command not recognized: ' + user_command)
            else:
                if len(correct_list) != len(user_command.split()) - 1:
                    flag = 0
                    print('Command not recognized: ' + user_command)
        else:
            if not user_command.split()[-2].isnumeric():
                if len(correct_list) != len(user_command.split()) - 1:
                    flag = 0
                    print('Command not recognized: ' + user_command)
            else:
                if len(correct_list) != len(user_command.split()) - 2:
                    flag = 0
                    print('Command not recognized: ' + user_command)

        if len(user_command.split()) >= 2:
            if user_command.split()[0] == 'countries' and user_command.split()[1].split('=')[0] == 'country':
                flag = 0
                print('Command not recognized: ' + user_command)
            if len(user_command) >= 2 and user_command.split()[0] == 'regions' and user_command.split()[1].split('=')[
                0] == 'region':
                flag = 0
                print('Command not recognized: ' + user_command)
        if flag == 0:
            continue
        command_res = process_command(user_command)
        #print(sep_command)
        print_list(user_command, command_res)
        sep_command=get_prase_list(user_command)
        if sep_command[-1] == 'barplot':
            x = []
            y = []
            if (sep_command[0] == 'bars'):
                if sep_command[3] == 'ratings':
                    for i in command_res:
                        x.append(i[0])
                        y.append(i[3])
                elif sep_command[3] == 'cocoa':
                    for i in command_res:
                        x.append(i[0])
                        y.append(i[4])
            elif (sep_command[0] == 'companies' or sep_command[0] == 'countries'):
                for i in command_res:
                    x.append(i[0])
                    y.append(i[2])
            elif (sep_command[0] == 'regions'):
                for i in command_res:
                    x.append(i[0])
                    y.append(i[1])

            bar_data = go.Bar(x=x, y=y)
            title = go.Layout(title="Result")
            fig = go.Figure(data=bar_data, layout=title)
            fig.show()

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()
