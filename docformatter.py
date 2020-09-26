answers = []
definitions = []

with open("hist151_test1_dates.txt") as file:
    lines = file.readlines()
    
    for eachline in lines:
        splittedlines = eachline.strip().split(";")
        if (splittedlines[1] == "to be found out***"):
            continue
        definitions.append(splittedlines[0])
        answers.append(splittedlines[1])

with open("changeMyFileName.txt", "w") as file:     
    for i in range(len(answers)):
        file.write(answers[i].strip() + "\t" + definitions[i].strip() + "\n")