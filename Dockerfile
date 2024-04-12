FROM python:3.9
RUN mkdir -p /opt/eval_des
WORKDIR /opt/eval_des
COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
CMD ["source", "venv/bin/activate"]
CMD ["python3", "app.py"]