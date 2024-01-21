# Verbal Regex(구어체 정규식)
정규식(정규 표현식)을 쉽게 작성하는 방법 <br>
The way makes easy to write regex

## Install 설치
```
pip install VerbalRegex
```
- [PyPI](https://example.com)

## Example 예시
- URL Regex / URL 정규식

```python
# URL Regex
from Package.VerbalRegex import VerRe

v = VerRe()
regex = v.start_of_line()
    .find('http')
    .maybe('s')
    .find('://')
    .anything()
    .repeatPreviousOver1()
    .end_of_line()

print(regex)  # ^(http)(s)?(://).+$
print(regex.match('https://example.com'))  # Matched(일치)
print(regex.match('httpss://example.com'))  # None(Not matched, 일치하지 않음)
```
## Usage 사용법
- [사용법 - 한국어](https://github.com/DM-09/Verbal-Regex.py/tree/main/Guide/%ED%95%9C%EA%B5%AD%EC%96%B4)
- [Usage - English](https://github.com/DM-09/Verbal-Regex.py/tree/main/Guide/English)