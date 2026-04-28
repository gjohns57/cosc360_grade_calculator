## COSC 360 Grade Calculator

Hit Ctrl-S on your grades page and save the html to this directory. Then run parse_grades.py

```
python -m venv .venv
source .venv/bin/activate
pip install .
python parse_grades.py
```
or
```
uv run parse_grades.py
```

You will get your computed final grade including only graded assignments as well as a csv that you can 
modify scores in to try different grades.
