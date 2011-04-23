def major_requirements(audit):
    class audit:
        audit_information = dict(audit.xpath('//AuditHeader')[0].items())
        sections = []
        for section in audit.xpath('//Block'):
            items = dict(section.items())
            formatted_items = {'Title':items['Title'], 'Percent Complete':items['Per_complete'], 'Credits Applied':items['Credits_applied'], 'Classes Applied':items['Classes_applied'], 'Requirement ID':items['Req_id'], 'Requirement Value':items['Req_value'], 'Requirement Type':items['Req_type'], 'GPA':items['GPA'], 'GPA Credits':items['Gpa_credits'], 'Cat_yr':items['Cat_yr'],'Cat_yr_start':items['Cat_yr_start'], 'Cat_yrLit':items['Cat_yrLit'], 'GPA points':items['Gpa_grade_pts']}
            sections.append(formatted_items)

    return audit


