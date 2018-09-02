#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
import json
import os


app = Flask(__name__)


evaluations = [
    {
        'id': 'povedomi',
        'question': 'Povědomí o co jde - náročnost, komplexita IT světa',
        'choices': [0, 1],
    }, {
        'id': 'stanoveny_cil',
        'question': 'Má stanovený cíl',
        'choices': [0, 1],
    }, {
        'id': 'pracovni_vyhlidky',
        'question': 'Nadějné pracovní vyhlídky',
        'choices': [0, 1],
    }, {
        'id': 'posun',
        'question': 'Kurz může posunout k cíli',
        'choices': [0, 1],
    }, {
        'id': 'samostatne_studium',
        'question': 'Potenciál k samostatnému studiu',
        'choices': [0, 1],
    }, {
        'id': 'socialni',
        'question': 'Zmínka o lidech a komunitě',
        'choices': [0, 1],
    }, {
        'id': 'predchozi_samostatna_snaha',
        'question': 'Předchozí samostatná snaha',
        'choices': [0, 1],
    }, {
        'id': 'predchozi_kurzy',
        'question': 'Předchozí snaha - jiné kurzy',
        'choices': [0, 1],
    }, {
        'id': 'redundantni_vs',
        'question': 'Redundantní - jde studovat VŠ',
        'choices': [0, -1],
    }, {
        'id': 'redundantni_jine',
        'question': 'Redundantní - něco jiného',
        'choices': [0, -1, -2],
    }, {
        'id': 'promarnene',
        'question': 'Měl(a) už "šanci", ale promarnil(a) ji',
        'choices': [0, -1],
    }, {
        'id': 'jenom_zkusit',
        'question': 'Chce to jen zkusit, "Tady mě máte", "rozvoj osobnosti"',
        'choices': [0, -1],
    }, {
        'id': 'dobry_pocit',
        'question': 'Dobrý pocit',
        'choices': [0, 1, 2],
    }, {
        'id': 'spatny_pocit',
        'question': 'Špatný pocit',
        'choices': [0, -1, -2],
    },
]


def load_regs():
    with open('registrace.json') as f:
        return json.load(f)


def load_evaluations():
    with open('evaluations.json') as f:
        ev_data = json.load(f)
    return {int(k): v for k, v in ev_data.items()}


def save_evaluations(data):
    with open('evaluations.json.temp', 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.rename('evaluations.json', 'evaluations.json.backup')
    os.rename('evaluations.json.temp', 'evaluations.json')
    print('Evaluations saved')


@app.route('/')
def index():
    regs = load_regs()
    return render_template('index.html', regs=regs)


@app.route('/<int:reg_id>')
def detail(reg_id):
    regs = load_regs()
    ev_data = load_evaluations()
    ev_answers = ev_data.get(reg_id) or {}
    (n, reg), = [(n, reg) for n, reg in enumerate(regs) if reg['id'] == reg_id]
    prev_reg = regs[n-1] if n > 0 else regs[0]
    next_reg = regs[n+1] if n + 1 < len(regs) else regs[0]
    return render_template('detail.html',
        reg=reg, prev_reg=prev_reg, next_reg=next_reg,
        evaluations=[{**ev, 'answer': ev_answers.get(ev['id'])} for ev in evaluations])


@app.route('/<int:reg_id>/submit-evaluation', methods=['POST'])
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
