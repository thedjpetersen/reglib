import reglib

###############
# INSTANTIATION
###############
reg_class = reglib.infosu('931596171', '544354')
#results = reg_class.make_schedule(['cs 321'], 'F11')

#for index, combination_list in enumerate(results):
#    print "Combination " + str(index+1)
#    for combination in combination_list:
#        print combination['Type'] + ' ' + combination['Dep'] + ' ' + combination['Num'] + ' ' + ('').join(combination['Day/Time/Date']['Days'])  + ' ' +  ('-').join(combination['Day/Time/Date']['Time']) + ' CRN: ' + combination['CRN']
#        print

##############
# TRANSCRIPT
##############
reg_class.get_transcript()
#print reg_class.transcript.sort_by_term()
#print reg_class.transcript.credits
#print reg_class.transcript.has_class('ph', '211') # Summary of class already passed
#print reg_class.transcript.has_passed_class('ph', '212') # Boolean
#print reg_class.transcript.grade_distribution()

#########
#SCHEDULE
#########
#print reg_class.schedule.current_classes
#print reg_class.schedule.schedule

##########
#SEARCHING
##########
#print reg_class.class_search('cs', '311')
#print reg_class.class_search_schedule('ph', '213')


###################
#POSSIBLE SCHEDULES
###################
#print reg_class.make_schedule(['cs 261', 'fr 213', 'cs 275', 'mth 232'])
#print reg_class.make_schedule(['cs 162', 'mth 111'], 'F12')


