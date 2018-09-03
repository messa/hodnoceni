FROM python:3-alpine

RUN pip install flask

WORKDIR /app

COPY . ./

EXPOSE 8000

CMD [ \
    "python3", "evaluation_web.py", \
    "--dataset", "dataset.json.sample", \
    "--questions", "questions.json.sample", \
    "--answers", "answers-sample.json" \
]

