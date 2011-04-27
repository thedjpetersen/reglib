class audit:
    def __init__(self, audit):
        self.audit_information = dict(audit.xpath('//AuditHeader')[0].items())
        self.sections = []
        self.required_classes = []
        
        for section in audit.xpath('//Block'):
            items = dict(section.items())
            formatted_items = {'Title':items['Title'], 'Percent Complete':items['Per_complete'], 'Credits Applied':items['Credits_applied'], 'Classes Applied':items['Classes_applied'], 'Requirement ID':items['Req_id'], 'Requirement Value':items['Req_value'], 'Requirement Type':items['Req_type'], 'GPA':items['GPA'], 'GPA Credits':items['Gpa_credits'], 'Cat_yr':items['Cat_yr'],'Cat_yr_start':items['Cat_yr_start'], 'Cat_yrLit':items['Cat_yrLit'], 'GPA points':items['Gpa_grade_pts']}
            rules = []

            for each_rule in section.xpath('Rule'):
                rules.append(rule(each_rule))

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

    
class rule:

    def __init__(self, rule):
        self.rule_type = rule.xpath('@RuleType')[0]
        if self.rule_type == 'Course':
            self.course_rule(rule)

    def course_rule(self, rule):
        rule_items = dict(rule.items())
        self.courses = []
        for course in rule.xpath('Advice/Course'):
            self.courses.append(dict(course.items()))
        self.name = rule_items['Label']
        self.percent_complete = rule_items['Per_complete']
        self.rule_id = rule_items['Rule_id']
        self.node_type = rule_items['Node_type']
        self.node_id = rule_items['Node_id']



