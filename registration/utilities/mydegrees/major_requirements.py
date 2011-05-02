class audit:
    def __init__(self, audit, advice):
        self.audit_information = dict(audit.xpath('//AuditHeader')[0].items())
        self.sections = []
        self.required_classes = []
        self.in_progress_classes = []
        self.completed_classes = []
        self.advice = advice

        for section in audit.xpath('//Block'):
            items = dict(section.items())
            formatted_items = {'Title':items['Title'], 'Percent Complete':items['Per_complete'], 'Credits Applied':items['Credits_applied'], 'Classes Applied':items['Classes_applied'], 'Requirement ID':items['Req_id'], 'Requirement Value':items['Req_value'], 'Requirement Type':items['Req_type'], 'GPA':items['GPA'], 'GPA Credits':items['Gpa_credits'], 'Cat_yr':items['Cat_yr'],'Cat_yr_start':items['Cat_yr_start'], 'Cat_yrLit':items['Cat_yrLit'], 'GPA points':items['Gpa_grade_pts']}
            rules = []

            for each_rule in section.xpath('Rule'):
                rule_class = rule(each_rule)
                rules.append(rule_class)
                self.class_assigner(rule_class) 

            formatted_items['Rules'] = rules
            self.sections.append(formatted_items)

            goals = []
            for item in audit.xpath('Deginfo/Goal'):
                goals.append(dict(item.items()))
            
            temp_dict = dict(audit.xpath('Deginfo/DegreeData')[0].items())
            self.degree_data = {}
            self.degree_data['Level'] = temp_dict['Stu_levelLit']
            self.degree_data['Degree'] = temp_dict['DegreeLit']
            self.degree_data['Degree Code'] = temp_dict['Degree']
            self.degree_data['School Code'] = temp_dict['School']
            self.degree_data['GPA'] = self.audit_information['DWGPA']
            self.degree_data['Classes'] = self.sections[0]['Classes Applied']
            self.degree_data['Credits'] = self.sections[0]['Credits Applied']
            self.degree_data['Email'] = self.audit_information['Stu_email']

            self.student_id = self.audit_information['Stu_id']
            self.audit_id = self.audit_information['Audit_id']

    def class_assigner(self, rule_class):
        if(rule_class.rule_type == 'Course'):
            if(rule_class.percent_complete == '0'):
                try:
                    rule_class.courses += self.advice[rule_class.advice_code]['Classes']
                except:
                    pass
                self.required_classes.append(rule_class)
            if(rule_class.percent_complete == '98'):
                self.in_progress_classes.append(rule_class)
            if(rule_class.percent_complete == '100'):
                self.completed_classes.append(rule_class)
        if(rule_class.rule_type == 'Subset'):
            for each_rule in rule_class.rules:
                self.class_assigner(each_rule)
        if(rule_class.rule_type == 'Group' and rule_class.percent_complete == '0'):
            rule_class.courses = []
            for each_rule in rule_class.rules:
                if(each_rule.rule_type == 'Course'):
                    rule_class.courses += each_rule.courses
                if(each_rule.rule_type == 'Group'):
                    self.class_assigner(each_rule)
            self.required_classes.append(rule_class)

class rule:

    def __init__(self, rule):
        self.rule_type = rule.xpath('@RuleType')[0]
        if self.rule_type == 'Course':
            self.course_rule(rule)
        if self.rule_type == 'Subset' or self.rule_type == 'Group':
            self.subset_group_rule(rule)
        if self.rule_type == 'IfStmt':
            self.if_rule(rule)

    def course_rule(self, rule):
        rule_items = dict(rule.items())
        requirement_items = dict(rule.xpath('Requirement')[0].items())
        try:
            self.classes_needed = requirement_items['Classes_begin']
            self.classes_option = requirement_items['Class_cred_op']
        except:
            pass

        try:
            self.advice_code = rule.xpath("RuleTag[@Name='AdviceJump']")[1].items()[1][1].split('#')[1]
        except:
            pass

        self.courses = []
        self.classes_applied = []
        for course in rule.xpath('Advice/Course'):
            self.courses.append(dict(course.items()))
        for applied_class in rule.xpath('ClassesApplied/Class'):
            items = dict(applied_class.items())
            self.classes_applied.append(items)
        self.name = rule_items['Label']
        self.percent_complete = rule_items['Per_complete']
        self.rule_id = rule_items['Rule_id']
        self.node_type = rule_items['Node_type']
        self.node_id = rule_items['Node_id']

    def subset_group_rule(self, rule):
        rule_items = dict(rule.items())
        self.name = rule_items['Label']
        self.percent_complete = rule_items['Per_complete']
        self.rule_id = rule_items['Rule_id']
        self.node_type = rule_items['Node_type']
        self.node_id = rule_items['Node_id']
        
        self.rules = []
        member_rules = rule.xpath('Rule')
        for each_rule in member_rules:
            self.rules.append(self.__class__(each_rule))

    def if_rule(self, rule):
        rule_items = dict(rule.items())
        if(rule_items['Per_complete'] != 'Not Used'):
            try:
                if not rule.xpath("Requirement/IfPart/Rule[@Per_complete='Not Used']"):
                    self.__init__(rule.xpath("Requirement/IfPart/Rule")[0])
                else:
                    self.__init__(rule.xpath("Requirement/ElsePart/Rule")[0])
            except:
                pass
