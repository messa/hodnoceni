#!/usr/bin/env python3

import argparse
from flask import Flask, Blueprint, render_template, request, redirect, g, abort
from functools import partial
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dataset', default='dataset.json')
    p.add_argument('--questions', default='questions.json')
    p.add_argument('--answers', default='answers.json')
    p.add_argument('--port', type=int, default=8000)
    args = p.parse_args()

    app = Flask(__name__)
    app.register_blueprint(bp)

    @app.before_request
    def register_stuff():
        g.datapoints = load_dataset(args.dataset)
        g.questions = load_questions(args.questions)
        g.answers = expand(load_answers(args.answers), len(g.datapoints))
        g.save_answers = partial(save_answers, args.answers)

    app.run(host='0.0.0.0', debug=False, use_evalex=False, port=args.port, threaded=True)


bp = Blueprint('main', __name__)


def load_questions(questions_path):
    try:
        questions = json.loads(Path(questions_path).read_text())
    except Exception as e:
        raise Exception(f'Failed to load {questions_path}: {e}')
    assert isinstance(questions, dict)
    return questions


def load_dataset(dataset_path):
    '''
    Load JSON or JSONL file.
    Returns list.
    '''
    s = Path(dataset_path).read_text().strip()
    if s.startswith('['):
        data = json.loads(s)
        assert isinstance(data, list)
    else:
        data = [json.loads(line) for line in s.splitlines()]
    return data


def load_answers(answers_path):
    try:
        answers = json.loads(Path(answers_path).read_text())
    except FileNotFoundError:
        answers = []
    assert isinstance(answers, list)
    return answers


def save_answers(answers_path, index, datapoint_answers):
    assert isinstance(index, int)
    answers = expand(load_answers(answers_path), index + 1)
    answers[index] = datapoint_answers
    temp = Path(answers_path + '.temp')
    temp.write_text(json.dumps(answers, indent=2, sort_keys=True))
    temp.rename(answers_path)


def expand(lst, min_length):
    return lst + [None] * max(0, min_length - len(lst))


@bp.route('/')
def index():
    return render_template('index.html', datapoints=g.datapoints)


@bp.route('/<int:point_id>')
def detail(point_id):
    return render_template('detail.html',
        point_id=point_id,
        datapoint=g.datapoints[point_id],
        questions=g.questions,
        datapoint_answers=g.answers[point_id] or {},
        previous_point_id=point_id - 1 if point_id > 0 else None,
        next_point_id=point_id + 1 if len(g.datapoints) > point_id + 1 else None)


@bp.route('/submit/<int:point_id>', methods=['POST'])
def submit_answers(point_id):
    answers = {q_id: request.form.get(q_id) for q_id in g.questions.keys()}
    g.save_answers(point_id, answers)
    if point_id + 1 < len(g.datapoints):
        return redirect('/{}'.format(point_id + 1))
    else:
        return redirect('/')


if __name__ == '__main__':
    main()
