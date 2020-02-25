import json
import re
import string
from datetime import datetime


console_caller = '[VAGAS_ANALYZER.PY]'
topics = [
    ' JAVA ',
    'RUBY',
    'PHP',
    'PYTHON',
    ' C ',
    'C++',
    'ANGULAR',
    'VUE',
    'LARAVEL',
    'C#',
    'NET',
    'REACTJS',
    'REACT NATIVE',
    'SWIFT',
    'SCRUM',
    'DOCKER',
    'HTML',
    'CSS',
    'JAVASCRIPT',
    'LINUX',
    'ASPNET',
    'JSON',
    'XML',
    'XAMARIN',
    'AUTO LAYOUT',
    'XIB',
    'STORYBOARD',
    "COREDATA",
    "REST",
    "GIT",
    "MVP",
    "RPA",
    'AUTOMATION ANYWHERE',
    'MICROSOFT SHAREPOINT',
    'MICROSOFT FLOW',
    "JSF",
    "EJB",
    "CDI",
    "JPA",

]


def read_from_json():
    with open('[VAGAS.PY]_raw_results.json') as json_file:
        return json.load(json_file)


def assemble_analysis_object(entry, detected_topics):
    temp_info = {
        "company_name": entry["company_name"],
        "job_title": entry["job_title"],
        "job_hierarchy": entry["job_hierarchy"],
        "wage": entry["wage"],
        "location": entry["location"],
        "detected_topics": detected_topics,
        "job_benefits": entry["job_benefits"],
        "timestamp": entry["timestamp"],
        "analysis_timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "date_posted": entry["date_posted"],
        "source_url": entry["source_url"],
        "source_site": "VAGAS.COM",
    }
    return temp_info


def analyze_job_requirements(parsed_data):
    analyzed_entries = []
    for entry in parsed_data:
        temp = json.dumps(entry["job_description"],
                          indent=4, ensure_ascii=False).upper()
        rx = re.compile('([&,.;!()\{\}])')
        temp = rx.sub(r'', temp)
        detected_topics = []
        for topic in topics:
            if topic in temp:
                detected_topics.append(topic)
        """ print(temp)
        break """
        analyzed_entries.append(
            assemble_analysis_object(entry, detected_topics))
    return analyzed_entries


def write_to_json(data_dict):
    with open(f"{console_caller}_analyzed_results.json", "w") as outfile:
        json.dump(data_dict, outfile, indent=4, ensure_ascii=False)


def main_handler():
    parsed_data = read_from_json()
    analyzed_entries = analyze_job_requirements(parsed_data)
    write_to_json(analyzed_entries)


main_handler()
