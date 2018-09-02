#!/usr/bin/env python3

import argparse
from flask import Flask, Blueprint, render_template, request, redirect, g
import json
import os


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dataset', default='dataset.json')
    p.add_argument('--questions', default='questions.json')
    p.add_argument('--answers', default='answers.json')
    p.add_argument('--port', type=int, default=8000)
    args = p.parse_args()

    def load_answers():
        answers = json.loads(Path(args.answers).read_text())


    def save_answers(index, datapoint_answers):
        assert isinstance(index, int)
        answers = load_answers()
        assert isinstance(results, list)
        while len(answers) <= index:
            answers.append(None)
        answers[index] = datapoint_answers
        temp = Path(args.answers + '.temp')
        temp.write_text(json.dumps(answers, indent=2, sort_keys=True))
        temp.rename(args.answers)

    app = Flask(__name__)
    app.register_blueprint(bp)

    @app.before_request
    def register_stuff():
        g.dataset = load_dataset(args.dataset)
        g.questions = json.loads(Path(args.questions).read_text())
        g.answers = json.loads(Path(args.answers).read_text())
        g.save_result = save_result

    app.run(host='0.0.0.0', debug=False, use_evalex=False, port=args.port, threaded=True)


bp = Blueprint('main', __name__)


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


@bp.route('/')
def index():
    return render_template('index.html', datapoints=g.datapoints)


@bp.route('/<int:point_id>')
def detail(point_id):
    return render_template('detail.html',
        datapoint=g.datapoints[point_id],
        datapoint_answers=)


    regs = load_regs()
    ev_data = load_evaluations()
    ev_answers = ev_data.get(reg_id) or {}
    (n, reg), = [(n, reg) for n, reg in enumerate(regs) if reg['id'] == reg_id]
    prev_reg = regs[n-1] if n > 0 else regs[0]
    next_reg = regs[n+1] if n + 1 < len(regs) else regs[0]
    return render_template('detail.html',
        reg=reg, prev_reg=prev_reg, next_reg=next_reg,
        evaluations=[{**ev, 'answer': ev_answers.get(ev['id'])} for ev in evaluations])


@bp.route('/<int:reg_id>/submit-evaluation', methods=['POST'])
def submit_evaluation(reg_id):
    ev_data = load_evaluations()
    answers = ev_data.setdefault(reg_id, {})
    for ev in evaluations:
        ev_id = ev['id']
        if request.form.get(ev_id):
            answer = int(request.form[ev_id])
            assert answer in ev['choices']
            answers[ev_id] = answer
    save_evaluations(ev_data)
    return redirect('/{}'.format(reg_id + 1))
