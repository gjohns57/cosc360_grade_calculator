## COSC 360 Grade Calculator

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Hit Ctrl-S on your grades page and save the html to this directory. Then run parse_grades.py

```
python parse_grades.py
```

You will get your computed final grade including only graded assignments as well as a csv that you can 
modify scores in to try different grades. This only computes your grade based on labs and exams maybe I
will update it as the semester goes on if anyone finds this useful.
