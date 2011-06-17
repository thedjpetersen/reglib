import reglib

###############
# INSTANTIATION
###############
reg_class = reglib.infosu('930608334', '121088')
#print reg_class
#result = reg_class.make_schedule(['ph 212'],'F11')
#for course in result:
#    print course

#for index, combination_list in enumerate(results):
#    print "Combination " + str(index+1)
#    for combination in combination_list:
#        print combination['Type'] + ' ' + combination['Dep'] + ' ' + combination['Num'] + ' ' + ('').join(combination['Day/Time/Date']['Days'])  + ' ' +  ('-').join(combination['Day/Time/Date']['Time']) + ' CRN: ' + combination['CRN']
#        print

##############
# TRANSCRIPT
##############
#reg_class.get_transcript()
#print reg_class.transcript.sort_by_term()
#print reg_class.transcript.credits
#print reg_class.transcript.has_class('ph', '211') # Summary of class already passed
#print reg_class.transcript.has_passed_class('ph', '212') # Boolean
#print reg_class.transcript.grade_distribution()

#########
#SCHEDULE
#########
#print reg_class.schedule.current_term
#print reg_class.schedule.current_classes
#print reg_class.schedule.schedule
#print reg_class.schedule.current_term
#print reg_class.next_schedule.current_classes
#print reg_class.next_schedule.schedule
#print reg_class.next_schedule.current_term

##########
#SEARCHING
##########
#print reg_class.class_search('cd', '311')
#print reg_class.class_search_schedule('ph', '213')


###################
#POSSIBLE SCHEDULES
###################
print "Permutations: " + str(len(reg_class.make_schedule(['cs 160', 'fr 211', 'cs 275', 'mth 231'])))
'''
combinations = ms['combinations']
classes_possible = ms['classes_possible']

for index, combination in enumerate(combinations):
    print "Combination " + str(index) 
    for course in combination:
        print ''.join(['(', course['type'],') ',course['department'],' ',course['number'],' ',course['crn']])
    print
'''
#print reg_class.make_schedule(['cs 162', 'mth 111'], 'F12')

##########
#MYDEGREES
##########
#audit = reg_class.get_major_requirements()
#print audit
#for instance in audit.required_classes:
#    for course in instance.courses:
#        print course

