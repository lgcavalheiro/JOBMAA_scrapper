from datetime import datetime
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import numpy
import json
import re
import nltk
from tinydb import TinyDB, Query
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


console_caller = '[VAGAS_ANALYZER.PY]'
topics = ''


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


def process_entry(entry):
    temp = entry['job_description'].upper()
    """ temp = json.dumps(entry["job_description"],
                      indent=4, ensure_ascii=False).upper() """
    temp = pre_process(temp)
    temp = filter_chunks(temp)
    temp = str(stringify_chunks(temp))
    temp = re.sub(r' \:\,\(\)\'\"\[\]\{\}\?\; ', ' ',  temp)
    return temp


def detect_topics(processed_entry):
    detected_topics = []
    for topic in topics:
        if type(topic) is dict:
            for subtopic in topic:
                if subtopic in processed_entry:
                    detected_topics.append(list(topic.keys())[0])
        else:
            if topic in processed_entry:
                detected_topics.append(topic)
    detected_topics = format_entry(detected_topics)
    return detected_topics


def analyze_job_requirements(parsed_data):
    analyzed_entries = []
    for entry in parsed_data:
        processed_entry = process_entry(entry)
        detected_topics = detect_topics(processed_entry)
        if len(detected_topics) > 0:
            analyzed_entries.append(
                assemble_analysis_object(entry, detected_topics))
    return analyzed_entries


def format_entry(analyzed_entries):
    if 'JAVA' in analyzed_entries:
        ct = 0
        for word in analyzed_entries:
            if 'JAVA' in word:
                ct += 1
        if ct >= 2:
            analyzed_entries.remove('JAVA')

    analyzed_entries = set(analyzed_entries)

    if 'SQL' in analyzed_entries and 'SQL SERVER' in analyzed_entries:
        analyzed_entries.remove('SQL')

    if ' R ' in analyzed_entries and 'R $' in analyzed_entries:
        analyzed_entries.remove(' R ')
        analyzed_entries.remove('R $')

    if 'R $' in analyzed_entries:
        analyzed_entries.remove('R $')

    return list(analyzed_entries)


def pre_process(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    np_rule = "CHUNK: {<JJ>?<NNP>?<NN>?<NNP>*<CD>*<.>*}"
    cp = nltk.RegexpParser(np_rule)
    cs = cp.parse(sent)
    return cs


def filter_chunks(data):
    chunks = []
    for d in data:
        if type(d) == nltk.tree.Tree:
            chunks.append(d)
    return chunks


def stringify_chunks(data):
    terms = []
    for e in data:
        if isinstance(e, tuple):
            terms.append([e[0]])
        else:
            terms.append([w for w, t in e])

    finalstring = []
    for t in terms:
        temp = ''
        for s in t:
            temp += str(s) + ' '
        temp = temp.strip()
        finalstring.append(temp)
        temp = ''
    return finalstring


def insert_db(data):
    db = TinyDB(console_caller+'_analyzed_results.json')
    Entry = Query()
    for entry in data:
        if db.search(Entry.identifier == entry['identifier']):
            pass
        else:
            print(
                f"{console_caller} New insert made: {entry['job_title']} - {entry['identifier']}")
            db.insert(entry)


def read_from_db(dbname):
    db = TinyDB(dbname)
    return db.all()


def read_from_json(file):
    with open(file) as json_file:
        return json.load(json_file)


def main_handler():
    global topics
    topics = read_from_json('topics.json')
    parsed_data = read_from_db('[VAGAS.PY]_raw_results.json')
    analyzed_entries = analyze_job_requirements(parsed_data)
    insert_db(analyzed_entries)


main_handler()
