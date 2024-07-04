import csv
import matplotlib.pyplot as plt
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
        if elem == 'none_background' or elem == 'none_bird' or elem == 'none_dirt' or elem == 'none_shadow':
            continue
        column = [int(row[elem]) for row in reader]
        count = column[0]       
        plt.figure(figsize=(10, 6))  # Increase the figure size to make the plot larger
        plt.plot(range(len(column)), column, label=elem)
        plt.xlabel('Frame')
        plt.ylabel('Number of elements')
        plt.title(f'{elem}')
        plt.legend()
        plt.axis([0, len(column)-1, -1, max(column) + 5])
        plt.savefig(f'PLOTS/figure_{elem}.png')
        plt.close()
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