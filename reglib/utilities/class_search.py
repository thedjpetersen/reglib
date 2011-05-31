import fetch_html
import parse_html

def class_search(dep, num, term=''):
        
        html = fetch_html.class_search(dep, num)
        if not html:
            return None #no such course

        # Get a array of available classes
        classes = parse_html.class_search(html, dep, num)
        if term is '':
            return classes
        
        # Get classes from certain term
        else:
            list_of_classes = []
            for each_class in classes:
                if each_class['Term'] == term:
                    #If the classes are in a certain term return them
                    list_of_classes.append(each_class)
            if len(list_of_classes) is not 0:
                return list_of_classes
            else:
                return None #no course for that term 
