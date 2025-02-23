import re

s = b'\n\n2'.decode()

number = re.search(r'\d+', s).group()

print(number)
