import sys

import requests
import json
from lxml.etree import HTML, tostring
from lxml import etree
from datetime import datetime
from itertools import chain

console_caller = "[VAGAS.PY]"


def root_request(url):
    r = requests.get(url)
    print(f"{console_caller} Requested: {r.url} - Status code: {r.status_code}")
    root = HTML(r.content)
    return root


def scrape_page(root, scrape_params):
    target_links = root.xpath(scrape_params)
    return target_links


def get_wage(target):
    wage = ""
    for element in target.iter("p", "ul", "strong", "li", "b", "span"):
        if element.text is not None:
            print(element.attrib)
            wage += " " + element.text
    return wage
    """ for child1 in target:
        if child1.tag == "ul":
            for child2 in child1:
                if child2.tag == "li":
                    for child3 in child2:
                        if child3.tag == "div":
                            for child4 in child3:
                                if child4.tag == "span":
                                    if child4.getchildren():
                                        return child4.text """


def get_description(root, target):
    el1 = scrape_page(root, target)[0]
    description = ""
    for element in el1.iter("p", "ul", "strong", "li"):
        if (
            element.text is not None
            and element.itertext()
            and type(element) is not list
            and str(element.text).lower().find("benefício") == -1
        ):
            for i in element.itertext():
                description += i
        elif str(element.text).lower().find("benefício") > -1:
            break
    return description


def get_benefits(root):
    article = scrape_page(root, '//article[@class="vaga"]')[0]
    benefits = ""
    found = False
    for element in article.iter("p", "ul", "strong", "li", "br"):
        if str(element.text).lower().find("benefício") > -1:
            found = True
        if found and element.text is not None:
            if element.tag == "p":
                break
            else:
                benefits += " " + element.text.replace("\n", "").strip()
    return benefits


def scrape_job_info(target_links):
    job_oportunities = []
    for target in target_links:
        root = root_request(f"https://www.vagas.com.br{target}")
        temp_info = {
            "company_name": scrape_page(
                root, '//h2[@class="job-shortdescription__company"]/text()'
            ),
            "job_title": scrape_page(
                root, '//h1[@class="job-shortdescription__title"]/text()'
            ),
            "job_hierarchy": scrape_page(
                root,
                '//li[@class="job-hierarchylist__item job-hierarchylist__item--level"]/@aria-label',
            ),
            "wage": get_wage(scrape_page(root, '//ul[@class="clearfix"]')[0]),
            "location": scrape_page(root, '//span[@class="info-localizacao"]/@title'),
            "job_description": get_description(root, '//div[@class="texto"]'),
            "job_benefits": get_benefits(root),
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "source_url": f"https://www.vagas.com.br{target}",
            "source_site": "VAGAS.COM",
        }
        for value in temp_info:
            if type(temp_info[value]) is list:
                temp = ""
                temp_info[value] = temp.join(temp_info[value])
            temp_info[value] = temp_info[value].replace("\n", "").strip()
        job_oportunities.append(temp_info)
        # break
    return job_oportunities


def write_to_json(data_dict):
    with open("results.json", "w") as outfile:
        json.dump(data_dict, outfile, indent=4, ensure_ascii=False)


def main_handler():
    url = "https://www.vagas.com.br/vagas-de-desenvolvedor-em-rio-de-janeiro"
    root = root_request(url)
    target_links = scrape_page(root, '//a[@class="link-detalhes-vaga"]/@href')
    job_oportunities = scrape_job_info(target_links)
    write_to_json(job_oportunities)


main_handler()

