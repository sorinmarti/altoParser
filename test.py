"""
address = ["Castle Mills",
           "Trafalgar",
           "Trafalgar Square",
           "Imperial Buildings",
           "Cambridge Street"]
address_list = sorted(address, key=len, reverse=True)


text = "3. misters at Trafalgar Square, W23, London 56ç%"
result = {}

for address in address_list:
    if address in text:
        result["location_found"] = True
        result["location"] = address
        break

print(result)
"""
import re

from main_1925 import readcsv

"""
import re
text = "45 Bartlett, F. H."
text2 = "946 Barnett, D."
text3 = "Alsnvsdv & Sons"
text4 = "August Fröhlich Textile Leathers, Belting and Machinery"
text5 = "  Pipe Lines (High Pressure)"
match = re.search(r'((\(.{1,150}\),? ))', text5)

if match:
    print(match)
    print(match.group(0))



""""""
name = ["LIST OF MEMBERS of the British Chamber of Commerce for Switzerland", "Page", "Address", "Trade and Name"]
text = "Trade and Name"

result = {}

for name in name:
    if name in text:
        result["name_found"] = True
        result["name"] = name
        break
print(result)
"""

from search_helper import SearchHelper
import csv
import os

companies = readcsv('meta/companies.csv')
companies_list = sorted(companies, key=len, reverse=True)

textt = "Aktiengesellschaft vorm. B. Siegfried (drugs & sundries), Zofingen."
searcher = SearchHelper("company")
searcher.set_search_list(companies_list)
searcher.set_pattern_list(["[Cc]astle [Mm]ills", "(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^ ?[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^ ?[A-Z]. \w{1,10}|.{1,100} Co\.)"])

result = searcher.search_in_list(textt)
print(result)
result = searcher.search(textt, priority=SearchHelper.LIST_BF_PATTERN, exit_after_match=True)
print(result)



"""
textt = "Ackroyd Brothers (wool, wool waste etc.), Imperial Buildings, Bradford."
searcher = SearchHelper("location")
searcher.set_search_list(["Ackroyd Brothers", "Trafalgar", "Castle mills",
                          "Trafalgar Square",
                          "Imperial Buildings",
                           "Cambridge Street", "Sulzer Frères S. A."])
searcher.set_pattern_list(["[Cc]astle [Mm]ills", "(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^ ?[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^ ?[A-Z]. \w{1,10}|.{1,100} Co\.)"])

result = searcher.search_in_list(textt)
print(result)
result = searcher.search(textt, priority=SearchHelper.LIST_BF_PATTERN, exit_after_match=False)
print(result)

"""