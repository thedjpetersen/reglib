import fetch_html
import parse_html
import mydegrees
from login import login

def get_major_requirements(sid, pin):
    """ use mydegrees to get various requirements to fulfill major such as
    courses needed """

    login_number = 2
    for i in range(login_number):
        html = fetch_html.infosu_mydegrees_redirect()

        if len(html) < 1000:
            login(sid, pin)
            continue

        form_list = parse_html.mydegrees_redirect_form(html)
        html = fetch_html.first_page_set_cookie(form_list)

        # Get variables from mydegrees
        form_list = parse_html.mydegrees_form_mangler(html)
        html = fetch_html.form_variables(form_list)

        # Get more variables from mydegrees
        form_list = parse_html.mydegrees_final_form(html)
        xml = fetch_html.get_xml(form_list)

        audit_tree = parse_html.get_major_requirements(xml)
        advice = parse_html.advice(fetch_html.advice())

        return mydegrees.audit(audit_tree, advice)
