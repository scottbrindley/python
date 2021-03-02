import string, random

letters = []
with open(r'C:\Users\scott\Documents\Python\data\letters_whites.txt', 'r') as f:
    reader = f.readlines() 
    for row in reader:
        letter = row
        letters.append(letter)  

letter_found = False
while letter_found is False:
        
    rand = random.choice(string.ascii_letters).lower()
    if rand in letters:
        print("letter " + rand + " already used")
    else:
        letter_found = True
        print("your letter for this week is.... " + rand.upper())
    
