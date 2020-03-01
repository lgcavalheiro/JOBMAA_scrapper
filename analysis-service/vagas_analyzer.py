from datetime import datetime
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy
import json
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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
        temp = pre_process(temp)
        temp = filter_chunks(temp)
        temp = str(stringify_chunks(temp))
        temp = re.sub(r' \:\,\(\)\'\"\[\]\{\}\?\; ', ' ',  temp)
        detected_topics = []
        for topic in topics:
            if type(topic) is dict:
                for t in topic:
                    if t in temp:
                        detected_topics.append(list(topic.keys())[0])
            else:
                if topic in temp:
                    detected_topics.append(topic)
        detected_topics = format_entry(detected_topics)
        # print(detected_topics)
        analyzed_entries.append(
            assemble_analysis_object(entry, detected_topics))
        # break
    return analyzed_entries


def format_entry(analyzed_entries):
    trueentries = analyzed_entries
    """ for a in analyzed_entries:
        if len(a) > 0:
            trueentries.append(a) """

    realtrueentries = analyzed_entries
    """ for e in trueentries:
        if len(e) > 1:
            for i in e:
                realtrueentries.append(str(i).replace(
                    '[', '').replace(']', '').replace('\'', ''))
        else:
            realtrueentries.append(str(e).replace(
                '[', '').replace(']', '').replace('\'', '')) """

    if 'JAVA' in realtrueentries:
        ct = 0
        for word in realtrueentries:
            if 'JAVA' in word:
                ct += 1
        if ct >= 2:
            realtrueentries.remove('JAVA')

    realtrueentries = set(realtrueentries)

    if 'C ' in realtrueentries and 'C #' in realtrueentries:
        realtrueentries.remove('C ')

    if 'C ' in realtrueentries and 'IONIC' in realtrueentries:
        realtrueentries.remove('C ')

    if 'SQL' in realtrueentries and 'SQL SERVER' in realtrueentries:
        realtrueentries.remove('SQL')

    if ' R ' in realtrueentries and 'R $' in realtrueentries:
        realtrueentries.remove(' R ')
        realtrueentries.remove('R $')

    if 'R $' in realtrueentries:
        realtrueentries.remove('R $')

    return list(realtrueentries)


def write_to_json(data_dict):
    with open(f"{console_caller}_analyzed_results.json", "w") as outfile:
        json.dump(data_dict, outfile, indent=4, ensure_ascii=False)


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


def main_handler():
    global topics
    topics = read_from_json('topics.json')
    parsed_data = read_from_json('[VAGAS.PY]_raw_results.json')
    analyzed_entries = analyze_job_requirements(parsed_data)
    write_to_json(analyzed_entries)


main_handler()
