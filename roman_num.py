
numbers_dict = {
    0:['zero','0','0'],
    1:['one','0','I'],
    2:['two','twenty','II'],
    3:['three','thirty','III'],
    4:['four','fourty','IV'],
    5:['five','fifty','V'],
    6:['six','sixty','VI'],
    7:['seven','seventy','VII'],
    8:['eight','eighty','VIII'],
    9:['nine','ninety','IX'],
    10:['ten','X'],
    11:['eleven'],
    12:['twelve'],
    13:['thirteen'],
    14:['fourteen'],
    15:['fifteen'],
    16:['sixteen'],
    17:['seventeen'],
    18:['eighteen'],
    19:['nineteen'],
    50:['L'],
    100:['C'],
    500:['D'],
    1000:['M']
}
def main():
    while True:
        try:
            user_input = int(input("Enter a number 0-999: "))
            break
        except(ValueError):
            print("Input must be an integer value.")
    print(parse_english(user_input))
    print(parse_roman(user_input))
    exit()

def parse_english(user_input):
    if user_input <= 19:        #zero-teens
        return numbers_dict[user_input][0]
    elif user_input <= 99:      #twenty-ninetynine
        singles = numbers_dict[user_input % 10][0]
        tens = numbers_dict[user_input // 10][1]
        if singles == 'zero':
            return tens
        return tens + '-' + singles
    else:                       #100-999
        hundreds_num = user_input // 100
        hundreds = numbers_dict[hundreds_num][0]
        user_input = user_input - (hundreds_num*100)
        if user_input == 0:
            return hundreds + ' hundred'
        if user_input > 10 and user_input <=19:
            return hundreds + 'hundred and ' + numbers_dict[user_input][0]
        tens = numbers_dict[user_input // 10][1]
        singles = numbers_dict[user_input % 10][0]
        if singles == 'zero':
            return hundreds + 'hundred' + tens 
        return hundreds + ' hundred and ' + tens + '-' + singles

def parse_roman(user_input):
    output = ''
    if user_input >= 500:
        if user_input >= 900:
            output += numbers_dict[100][0] + numbers_dict[1000][0]
            user_input -= 900
        else:
            output = output + numbers_dict[500][0]
            user_input -= 500
    while user_input >= 100:
        if user_input >= 400:
            output += numbers_dict[100][0] + numbers_dict[500][0]
            user_input -= 400
        else:
            output += numbers_dict[100][0]
            user_input -= 100
    while user_input >= 50:
        if user_input >= 90:
            output += numbers_dict[50][0] + numbers_dict[100][0]
            user_input -= 90
        else:    
            output += numbers_dict[50][0]
            user_input -= 50
    while user_input >= 10:
        if user_input >= 40:
            output += numbers_dict[10][1] + numbers_dict[50][0]
            user_input -= 40
        else:
            output += numbers_dict[10][1]
            user_input -= 10
    if user_input != 0:
        output += numbers_dict[user_input][2]

    return output

if __name__ == "__main__":
    main()