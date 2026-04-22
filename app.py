from flask import Flask, render_template, request, session, redirect, url_for
import math

app = Flask(__name__)
app.secret_key = 'researcher-tycoon-2024'

def fmt_p(p_str):
    try:
        p = float(p_str)
        if p < 0.001:
            return "p < .001"
        elif p < 0.01:
            return "p < .01"
        elif p < 0.05:
            return "p < .05"
        else:
            return "p = " + str(round(p, 3))
    except:
        return p_str

def fmt_r2(v):
    try:
        return str(round(float(v), 3))
    except:
        return v

RAW_RESULTS = {
    ("sd","2","log","lmm-full"):              {"coef":"-0.0364","p":"5.085e-22","n":"148,433","r2m":"0.343","r2c":"0.557"},
    ("sd","2","log","lmm-intercept"):         {"coef":"-0.0376","p":"1.201e-107","n":"148,433","r2m":"0.327","r2c":"0.542"},
    ("sd","2","log","lmm-intercept-slope"):   {"coef":"-0.0356","p":"3.357e-99","n":"148,433","r2m":"0.337","r2c":"0.557"},
    ("sd","2","raw","lmm-full"):              {"coef":"-18.19 ms","p":"3.236e-22","n":"148,433","r2m":"0.333","r2c":"0.566"},
    ("sd","2","raw","lmm-intercept"):         {"coef":"-18.67 ms","p":"1.017e-99","n":"148,433","r2m":"0.328","r2c":"0.537"},
    ("sd","2","raw","lmm-intercept-slope"):   {"coef":"-17.63 ms","p":"2.316e-91","n":"148,433","r2m":"0.327","r2c":"0.567"},
    ("sd","3","log","lmm-full"):              {"coef":"-0.0342","p":"1.994e-19","n":"154,173","r2m":"0.308","r2c":"0.501"},
    ("sd","3","log","lmm-intercept"):         {"coef":"-0.0353","p":"7.325e-80","n":"154,173","r2m":"0.294","r2c":"0.486"},
    ("sd","3","log","lmm-intercept-slope"):   {"coef":"-0.0334","p":"2.83e-73","n":"154,173","r2m":"0.303","r2c":"0.501"},
    ("sd","3","raw","lmm-full"):              {"coef":"-17.03 ms","p":"1.412e-18","n":"154,173","r2m":"0.293","r2c":"0.500"},
    ("sd","3","raw","lmm-intercept"):         {"coef":"-17.49 ms","p":"1.426e-69","n":"154,173","r2m":"0.287","r2c":"0.473"},
    ("sd","3","raw","lmm-intercept-slope"):   {"coef":"-16.50 ms","p":"2.536e-63","n":"154,173","r2m":"0.288","r2c":"0.502"},
    ("accuracy","0.6","log","lmm-full"):      {"coef":"-0.0183","p":"2.106e-08","n":"185,628","r2m":"0.222","r2c":"0.353"},
    ("accuracy","0.6","log","lmm-intercept"): {"coef":"-0.0183","p":"3.537e-19","n":"185,628","r2m":"0.215","r2c":"0.349"},
    ("accuracy","0.6","log","lmm-intercept-slope"): {"coef":"-0.0183","p":"2.277e-19","n":"185,628","r2m":"0.220","r2c":"0.354"},
    ("accuracy","0.6","raw","lmm-full"):      {"coef":"-9.36 ms","p":"1.751e-08","n":"185,628","r2m":"0.217","r2c":"0.364"},
    ("accuracy","0.6","raw","lmm-intercept"): {"coef":"-9.33 ms","p":"2.49e-18","n":"185,628","r2m":"0.213","r2c":"0.349"},
    ("accuracy","0.6","raw","lmm-intercept-slope"): {"coef":"-9.33 ms","p":"1.674e-18","n":"185,628","r2m":"0.215","r2c":"0.366"},
    ("accuracy","0.7","log","lmm-full"):      {"coef":"-0.0185","p":"2.169e-08","n":"182,466","r2m":"0.223","r2c":"0.353"},
    ("accuracy","0.7","log","lmm-intercept"): {"coef":"-0.0185","p":"1.733e-19","n":"182,466","r2m":"0.216","r2c":"0.349"},
    ("accuracy","0.7","log","lmm-intercept-slope"): {"coef":"-0.0185","p":"1.146e-19","n":"182,466","r2m":"0.221","r2c":"0.354"},
    ("accuracy","0.7","raw","lmm-full"):      {"coef":"-9.52 ms","p":"1.515e-08","n":"182,466","r2m":"0.218","r2c":"0.363"},
    ("accuracy","0.7","raw","lmm-intercept"): {"coef":"-9.47 ms","p":"9.335e-19","n":"182,466","r2m":"0.214","r2c":"0.347"},
    ("accuracy","0.7","raw","lmm-intercept-slope"): {"coef":"-9.47 ms","p":"6.365e-19","n":"182,466","r2m":"0.216","r2c":"0.364"},
    ("accuracy","0.8","log","lmm-full"):      {"coef":"-0.0195","p":"2.37e-08","n":"167,193","r2m":"0.231","r2c":"0.359"},
    ("accuracy","0.8","log","lmm-intercept"): {"coef":"-0.0195","p":"3.643e-21","n":"167,193","r2m":"0.222","r2c":"0.355"},
    ("accuracy","0.8","log","lmm-intercept-slope"): {"coef":"-0.0195","p":"2.411e-21","n":"167,193","r2m":"0.228","r2c":"0.360"},
    ("accuracy","0.8","raw","lmm-full"):      {"coef":"-10.03 ms","p":"2.389e-08","n":"167,193","r2m":"0.222","r2c":"0.367"},
    ("accuracy","0.8","raw","lmm-intercept"): {"coef":"-10.01 ms","p":"7.81e-20","n":"167,193","r2m":"0.218","r2c":"0.351"},
    ("accuracy","0.8","raw","lmm-intercept-slope"): {"coef":"-10.01 ms","p":"5.16e-20","n":"167,193","r2m":"0.220","r2c":"0.369"},
    ("no-filter","None","log","lmm-full"):      {"coef":"-0.0183","p":"1.745e-08","n":"192,713","r2m":"0.222","r2c":"0.422"},
    ("no-filter","None","log","lmm-intercept"): {"coef":"-0.0181","p":"5.445e-18","n":"192,713","r2m":"0.220","r2c":"0.403"},
    ("no-filter","None","log","lmm-intercept-slope"): {"coef":"-0.0182","p":"2.358e-18","n":"192,713","r2m":"0.220","r2c":"0.421"},
    ("no-filter","None","raw","lmm-full"):      {"coef":"-9.24 ms","p":"1.584e-08","n":"192,713","r2m":"0.219","r2c":"0.408"},
    ("no-filter","None","raw","lmm-intercept"): {"coef":"-9.13 ms","p":"1.463e-17","n":"192,713","r2m":"0.218","r2c":"0.383"},
    ("no-filter","None","raw","lmm-intercept-slope"): {"coef":"-9.18 ms","p":"6.611e-18","n":"192,713","r2m":"0.217","r2c":"0.409"},
}

TREE = {
    "step1": {
        "id": "step1", "step": 1, "total_steps": 4,
        "title": "Step 1 — Outlier Method",
        "question": "How do you want to handle outlier trials?",
        "description": (
            "Before modelling, you need to decide how to treat trials with unusual reaction times. "
            "You can remove trials based on how far they deviate from each participant's mean RT "
            "(z-score method), remove trials where the participant made an error (accuracy filter), "
            "or keep all trials without any filtering."
        ),
        "options": [
            {"label": "Z-score filter (remove trials beyond a threshold SD)", "value": "sd",
             "hint": "Removes outlier RTs per participant based on standard deviations.",
             "next": "step2_sd"},
            {"label": "Accuracy filter (remove incorrect trials only)", "value": "accuracy",
             "hint": "Keeps only trials where the participant responded correctly.",
             "next": "step2_acc"},
            {"label": "No filter (keep all trials)", "value": "no-filter",
             "hint": "No trial-level exclusion is applied.",
             "next": "step3_nf"},
        ]
    },

    "step2_sd": {
        "id": "step2_sd", "step": 2, "total_steps": 4,
        "title": "Step 2 — SD Threshold",
        "question": "What z-score threshold do you use to remove outlier trials?",
        "description": (
            "Trials are removed if a participant's RT on that trial falls more than N standard "
            "deviations from their mean. A threshold of 2 removes more trials (stricter), "
            "while 3 removes fewer (more lenient)."
        ),
        "options": [
            {"label": "2 SD threshold", "value": "2",
             "hint": "Stricter — removes more trials. n = 148,433 trials remaining.",
             "next": "step3_sd2"},
            {"label": "3 SD threshold", "value": "3",
             "hint": "More lenient — fewer trials removed. n = 154,173 trials remaining.",
             "next": "step3_sd3"},
        ]
    },

    "step2_acc": {
        "id": "step2_acc", "step": 2, "total_steps": 4,
        "title": "Step 2 — Accuracy Threshold",
        "question": "What minimum accuracy do you require to include a participant?",
        "description": (
            "Participants whose overall accuracy falls below the chosen threshold are excluded "
            "from the analysis entirely. A lower threshold retains more participants but includes "
            "those with high error rates. A higher threshold yields a cleaner sample."
        ),
        "options": [
            {"label": "60% minimum accuracy", "value": "0.6",
             "hint": "Lenient — n = 185,628 trials remaining.",
             "next": "step3_acc06"},
            {"label": "70% minimum accuracy", "value": "0.7",
             "hint": "Balanced — n = 182,466 trials remaining.",
             "next": "step3_acc07"},
            {"label": "80% minimum accuracy", "value": "0.8",
             "hint": "Strict — n = 167,193 trials remaining.",
             "next": "step3_acc08"},
        ]
    },

    "step3_nf": {
        "id": "step3_nf", "step": 3, "total_steps": 4,
        "title": "Step 3 — RT Transformation",
        "question": "Should reaction times be transformed before modelling?",
        "description": (
            "RT distributions are typically right-skewed. Log-transforming normalises the "
            "distribution and stabilises variance. Keeping raw milliseconds is more interpretable "
            "but may violate model assumptions."
        ),
        "outlier_key": "no-filter", "threshold_key": "None",
        "options": [
            {"label": "Log-transform RT", "value": "log", "hint": "Reduces skew. Unit is log(ms).", "next": "step4_nf_log"},
            {"label": "Keep raw RT (ms)", "value": "raw", "hint": "Directly interpretable in milliseconds.", "next": "step4_nf_raw"},
        ]
    },
    "step3_sd2": {
        "id": "step3_sd2", "step": 3, "total_steps": 4,
        "title": "Step 3 — RT Transformation",
        "question": "Should reaction times be transformed before modelling?",
        "description": (
            "RT distributions are typically right-skewed. Log-transforming normalises the "
            "distribution and stabilises variance. Keeping raw milliseconds is more interpretable "
            "but may violate model assumptions."
        ),
        "outlier_key": "sd", "threshold_key": "2",
        "options": [
            {"label": "Log-transform RT", "value": "log", "hint": "Reduces skew. Unit is log(ms).", "next": "step4_sd2_log"},
            {"label": "Keep raw RT (ms)", "value": "raw", "hint": "Directly interpretable in milliseconds.", "next": "step4_sd2_raw"},
        ]
    },
    "step3_sd3": {
        "id": "step3_sd3", "step": 3, "total_steps": 4,
        "title": "Step 3 — RT Transformation",
        "question": "Should reaction times be transformed before modelling?",
        "description": (
            "RT distributions are typically right-skewed. Log-transforming normalises the "
            "distribution and stabilises variance. Keeping raw milliseconds is more interpretable "
            "but may violate model assumptions."
        ),
        "outlier_key": "sd", "threshold_key": "3",
        "options": [
            {"label": "Log-transform RT", "value": "log", "hint": "Reduces skew. Unit is log(ms).", "next": "step4_sd3_log"},
            {"label": "Keep raw RT (ms)", "value": "raw", "hint": "Directly interpretable in milliseconds.", "next": "step4_sd3_raw"},
        ]
    },
    "step3_acc06": {
        "id": "step3_acc06", "step": 3, "total_steps": 4,
        "title": "Step 3 — RT Transformation",
        "question": "Should reaction times be transformed before modelling?",
        "description": (
            "RT distributions are typically right-skewed. Log-transforming normalises the "
            "distribution and stabilises variance. Keeping raw milliseconds is more interpretable "
            "but may violate model assumptions."
        ),
        "outlier_key": "accuracy", "threshold_key": "0.6",
        "options": [
            {"label": "Log-transform RT", "value": "log", "hint": "Reduces skew. Unit is log(ms).", "next": "step4_acc06_log"},
            {"label": "Keep raw RT (ms)", "value": "raw", "hint": "Directly interpretable in milliseconds.", "next": "step4_acc06_raw"},
        ]
    },
    "step3_acc07": {
        "id": "step3_acc07", "step": 3, "total_steps": 4,
        "title": "Step 3 — RT Transformation",
        "question": "Should reaction times be transformed before modelling?",
        "description": (
            "RT distributions are typically right-skewed. Log-transforming normalises the "
            "distribution and stabilises variance. Keeping raw milliseconds is more interpretable "
            "but may violate model assumptions."
        ),
        "outlier_key": "accuracy", "threshold_key": "0.7",
        "options": [
            {"label": "Log-transform RT", "value": "log", "hint": "Reduces skew. Unit is log(ms).", "next": "step4_acc07_log"},
            {"label": "Keep raw RT (ms)", "value": "raw", "hint": "Directly interpretable in milliseconds.", "next": "step4_acc07_raw"},
        ]
    },
    "step3_acc08": {
        "id": "step3_acc08", "step": 3, "total_steps": 4,
        "title": "Step 3 — RT Transformation",
        "question": "Should reaction times be transformed before modelling?",
        "description": (
            "RT distributions are typically right-skewed. Log-transforming normalises the "
            "distribution and stabilises variance. Keeping raw milliseconds is more interpretable "
            "but may violate model assumptions."
        ),
        "outlier_key": "accuracy", "threshold_key": "0.8",
        "options": [
            {"label": "Log-transform RT", "value": "log", "hint": "Reduces skew. Unit is log(ms).", "next": "step4_acc08_log"},
            {"label": "Keep raw RT (ms)", "value": "raw", "hint": "Directly interpretable in milliseconds.", "next": "step4_acc08_raw"},
        ]
    },
}

MODEL_STEP_TEMPLATE = {
    "step": 4, "total_steps": 4,
    "title": "Step 4 — Model Structure",
    "question": "Which random-effects structure do you use in the linear mixed model?",
    "description": (
        "Linear mixed models account for the repeated-measures structure by including "
        "participant-level random effects. More complex structures are more defensible "
        "but can fail to converge. The intercept-slope model is typically recommended."
    ),
    "options": [
        {"label": "Random intercept only", "value": "lmm-intercept",
         "hint": "Simplest structure — controls for baseline RT differences between participants."},
        {"label": "Random intercept + slope (congruency)", "value": "lmm-intercept-slope",
         "hint": "Recommended — allows the congruency effect to vary per participant."},
        {"label": "Full random effects", "value": "lmm-full",
         "hint": "Most complex — may not converge on smaller datasets."},
    ]
}

STEP4_NODES = {
    "step4_nf_log":    ("no-filter","None","log"),
    "step4_nf_raw":    ("no-filter","None","raw"),
    "step4_sd2_log":   ("sd","2","log"),
    "step4_sd2_raw":   ("sd","2","raw"),
    "step4_sd3_log":   ("sd","3","log"),
    "step4_sd3_raw":   ("sd","3","raw"),
    "step4_acc06_log": ("accuracy","0.6","log"),
    "step4_acc06_raw": ("accuracy","0.6","raw"),
    "step4_acc07_log": ("accuracy","0.7","log"),
    "step4_acc07_raw": ("accuracy","0.7","raw"),
    "step4_acc08_log": ("accuracy","0.8","log"),
    "step4_acc08_raw": ("accuracy","0.8","raw"),
}

for node_id, (om, thr, rt) in STEP4_NODES.items():
    node = dict(MODEL_STEP_TEMPLATE)
    node["id"] = node_id
    node["outlier_key"] = om
    node["threshold_key"] = thr
    node["rt_key"] = rt
    opts = []
    for opt in MODEL_STEP_TEMPLATE["options"]:
        o = dict(opt)
        result_key = (om, thr, rt, opt["value"])
        res = RAW_RESULTS.get(result_key, {})
        result_node_id = "result_" + node_id[6:] + "_" + opt["value"].replace("-","_")
        o["next"] = result_node_id
        o["result_key"] = result_key
        opts.append(o)
    node["options"] = opts
    TREE[node_id] = node

RESULT_NODES = {}
for node_id, (om, thr, rt) in STEP4_NODES.items():
    for model in ["lmm-intercept","lmm-intercept-slope","lmm-full"]:
        result_node_id = "result_" + node_id[6:] + "_" + model.replace("-","_")
        key = (om, thr, rt, model)
        res = RAW_RESULTS.get(key, {})
        p_raw = res.get("p","")
        p_fmt = fmt_p(p_raw)
        sig = float(p_raw) < 0.05 if p_raw else False
        outlier_labels = {"sd": "Z-score (SD)", "accuracy": "Accuracy filter", "no-filter": "No filter"}
        model_labels = {"lmm-intercept": "Random intercept", "lmm-intercept-slope": "Intercept + slope", "lmm-full": "Full random effects"}
        RESULT_NODES[result_node_id] = {
            "id": result_node_id,
            "step": 5,
            "is_result": True,
            "outlier_method": om,
            "threshold": thr,
            "rt_transform": rt,
            "model": model,
            "outlier_label": outlier_labels.get(om, om),
            "model_label": model_labels.get(model, model),
            "coef": res.get("coef","—"),
            "p_raw": p_raw,
            "p_fmt": p_fmt,
            "significant": sig,
            "n": res.get("n","—"),
            "r2m": res.get("r2m","—"),
            "r2c": res.get("r2c","—"),
        }

TREE.update(RESULT_NODES)

ORIGINAL_PATH = {
    "outlier": "accuracy",
    "threshold": "0.7",
    "transform": "log",
    "model": "lmm-intercept-slope"
}


@app.route('/')
def welcome():
    session.clear()
    return render_template('welcome.html')

@app.route('/study')
def study():
    return render_template('study.html')

@app.route('/game')
def game():
    session.setdefault('path', [])
    node_id = request.args.get('node', 'step1')
    node = TREE.get(node_id)
    if not node:
        return redirect(url_for('game'))
    return render_template('game.html', node=node, path=session.get('path', []))

@app.route('/choose', methods=['POST'])
def choose():
    node_id = request.form.get('node_id')
    choice  = request.form.get('choice')
    node    = TREE.get(node_id)
    if not node:
        return redirect(url_for('game'))
    chosen = next((o for o in node.get('options', []) if o['value'] == choice), None)
    if not chosen:
        return redirect(url_for('game', node=node_id))
    path = session.get('path', [])
    path.append({
        'step':     node['step'],
        'node_id':  node_id,
        'title':    node['title'],
        'question': node['question'],
        'choice':   chosen['label'],
        'value':    chosen['value'],
        'hint':     chosen.get('hint',''),
        'next':     chosen['next'],
    })
    session['path'] = path
    session.modified = True
    return redirect(url_for('game', node=chosen['next']))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('welcome'))

@app.route('/end')
def end():
    path = session.get('path', [])
    result_node_id = path[-1]['next'] if path else None
    result = TREE.get(result_node_id) if result_node_id else None
    orig_key = (ORIGINAL_PATH['outlier'], ORIGINAL_PATH['threshold'], ORIGINAL_PATH['transform'], ORIGINAL_PATH['model'])
    orig_result = RAW_RESULTS.get(orig_key, {})
    orig_p = fmt_p(orig_result.get('p',''))
    raw_results_js = {",".join(k): v for k, v in RAW_RESULTS.items()}
    return render_template('end.html', path=path, result=result, original=ORIGINAL_PATH, orig_result=orig_result, orig_p=orig_p, raw_results=raw_results_js)

if __name__ == '__main__':
    app.run(debug=True)
