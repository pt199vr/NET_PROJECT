import csv
import matplotlib.pyplot as plt
import os

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

def counter(path_to_csv, path_to_stats, path_to_plots):
    print(path_to_csv, path_to_stats)
    # Open the CSV file
    with open(path_to_csv, 'r') as file:
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
            plt.savefig(f'{path_to_plots}figure_{elem}.png')
            plt.close()
            for i in range(1, len(column)): 
                if column[i] > column[i - 1]: 
                    count +=  column[i] - column[i - 1]
            
            print(count)
            with open(path_to_stats, 'w') as file:
                for elem in class_labels:
                    column = [int(row[elem]) for row in reader]
                    count = column[0]
                    for i in range(1, len(column)):
                        if column[i] > column[i - 1]:
                            count += column[i] - column[i - 1]
                    
                    file.write(f'{elem}: {count}\n')

# Path to the source directory
path_to_source = 'INSETTI/'

for day in os.listdir(path_to_source):
    # Construct the full path
    day_path = os.path.join(path_to_source, day)
    for ft in os.listdir(day_path):
        ft_path = os.path.join(day_path, ft)
        # Check if the entry is a directory
        if os.path.isdir(ft_path):
            # List all files in the directory
            files = os.listdir(ft_path)

            final_path = ft_path + '/results/'
            directory_path = final_path + 'plots/'
            
            if os.path.isdir(final_path):
                # Create the directory if it does not exist
                os.makedirs(directory_path, exist_ok=True)
                # Call the Classify function with the directory path and .csv file path
                counter(final_path + 'results.csv', final_path + 'stats.txt', directory_path)