FROM python:3.8

COPY algorithm.py config.json errors.py main.py object.py rule_base_condition.py requirements.txt ./
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
