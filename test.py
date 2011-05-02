import registration
test = registration.infosu('930608334', '121088')
results = test.make_schedule(['cs 261', 'fr 213', 'cs 275', 'mth 232'])

for index, combination_list in enumerate(results):
    print "Combination " + str(index+1)
    for combination in combination_list:
        print combination['Type'] + ' ' + combination['Dep'] + ' ' + combination['Num'] + ' ' + ('').join(combination['Day/Time/Date']['Days'])  + ' ' +  ('-').join(combination['Day/Time/Date']['Time']) + ' CRN: ' + combination['CRN']
    print
