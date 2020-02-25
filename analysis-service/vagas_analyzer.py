import json
import re
from datetime import datetime


console_caller = '[VAGAS_ANALYZER.PY]'
topics = ''


def read_from_json(file):
    with open(file) as json_file:
        return json.load(json_file)


def assemble_analysis_object(entry, detected_topics):
    temp_info = {
        "company_name": entry["company_name"],
        "identifier": entry["identifier"],
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
        rx = re.compile('([&,.;!()\{\}]:)')
        temp = rx.sub(r' ', temp)
        detected_topics = []
        for topic in topics:
            if topic in temp:
                detected_topics.append(topic)
        analyzed_entries.append(
            assemble_analysis_object(entry, detected_topics))
    return analyzed_entries


def write_to_json(data_dict):
    with open(f"{console_caller}_analyzed_results.json", "w") as outfile:
        json.dump(data_dict, outfile, indent=4, ensure_ascii=False)


def main_handler():
    global topics
    topics = read_from_json('topics.json')
    parsed_data = read_from_json('[VAGAS.PY]_raw_results.json')
    analyzed_entries = analyze_job_requirements(parsed_data)
    write_to_json(analyzed_entries)


main_handler()
