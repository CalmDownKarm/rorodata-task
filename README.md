# rorodata-task
Quick Web scraper for Rorodata's test

Written in Python 3
Uses Click, Beautifulsoup and Requests

## Usage

Query 1
```
python shoppingscraper.py [keywords]
``` 
Multi word keywords are allowed, as are special characters and numbers, provided website has products that match the keyword

Query 2
```
python shoppingscraper.py --pg [page number] [keywords]
```
float page numbers will be rounded off and converted to ints
