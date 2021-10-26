import numpy as np
import csv
rand = np.random

line = 100
header = ['Age', 'Size', 'Weight', 'number of victory','number of match','number of loose', 'number of equality', 'number of round to win', 'hit Area']
hitArea = ['top','mid','bot']

with open('df.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for i in range (0,line):
        data = [rand.randint(20,50),
                rand.randint(150,200),
                rand.randint(80,100),
                rand.randint(0,10),
                rand.randint(0,10),
                rand.randint(0,10),
                rand.randint(0,10),
                rand.randint(0,5),
                rand.choice(hitArea)]

        # write the data
        writer.writerow(data)