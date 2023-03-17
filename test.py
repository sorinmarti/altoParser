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
text = " MAURICE GALLAND Esq., Lausanne Vice-President"
match = re.search(r'(^[A-Z]\. ([A-Z]\.)? ?\w{1,100}|^[A-Z]{1,10} [A-Z]{1,10})', text)

if match:
    print(match)
    print(match.group(0))