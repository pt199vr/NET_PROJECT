import csv

class_labels = [
        'ant',
        'bee',
        'bee_apis',
        'bee_bombus',
        'beetle',
        'beetle_cocci',
        'beetle_oedem',
        'bug',
        'bug_grapho',
        'fly',
        'fly_empi',
        'fly_sarco',
        'fly_small',
        'hfly_episyr',
        'hfly_eristal',
        'hfly_eupeo',
        'hfly_myathr',
        'hfly_sphaero',
        'hfly_syrphus',
        'lepi',
        'none_background',
        'none_bird',
        'none_dirt',
        'none_shadow',
        'other',
        'scorpionfly',
        'wasp'
    ]

# Open the CSV file
with open('results.csv', 'r') as file:
    reader = list(csv.DictReader(file))

    for elem in class_labels:
        column = [int(row[elem]) for row in reader]
        count = column[0]
        for i in range(1, len(column)): 
            if column[i] > column[i - 1]: 
                count +=  column[i] - column[i - 1]
        
        print(count)
        with open('statistics.txt', 'w') as file:
            for elem in class_labels:
                column = [int(row[elem]) for row in reader]
                count = column[0]
                for i in range(1, len(column)):
                    if column[i] > column[i - 1]:
                        count += column[i] - column[i - 1]
                
                file.write(f'{elem}: {count}\n')