from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)


problems = {
    1: {
        "title": "Identity",
        "statement": "Prove that if P is true, then P is true.",
        "context": "",
        "theorem": "forall P : Prop, P -> P"
    },

    2: {
        "title": "First Projection",
        "statement": "Prove that if P and Q are true, then P is true.",
        "context": "",
        "theorem": "forall P Q : Prop, P -> Q -> P"
    },

    3: {
        "title": "Conjunction",
        "statement": "Prove that if P and Q are true, then P and Q are both true.",
        "context": "",
        "theorem": "forall P Q : Prop, P -> Q -> P /\\ Q"
    },

    4: {
        "title": "Conjunction Elimination",
        "statement": "Prove that if P and Q are both true, then P is true.",
        "context": "",
        "theorem": "forall P Q : Prop, P /\\ Q -> P"
    },

    5: {
        "title": "Implication Chaining",
        "statement": "If P implies Q and Q implies R, prove that P implies R.",
        "context": "",
        "theorem": "forall P Q R : Prop, (P -> Q) -> (Q -> R) -> P -> R"
    },

    6: {
        "title": "Modus Tollens",
        "statement": "If P implies Q and Q is false, prove that P is false.",
        "context": "",
        "theorem": "forall P Q : Prop, (P -> Q) -> ~Q -> ~P"
    },

    7: {
        "title": "Equivalence",
        "statement": "If P implies Q and Q implies P, prove that P and Q are logically equivalent.",
        "context": "",
        "theorem": "forall P Q : Prop, (P -> Q) -> (Q -> P) -> (P <-> Q)"
    },

    8: {
        "title": "Using an Equivalence",
        "statement": "If P is logically equivalent to Q and P is true, prove that Q is true.",
        "context": "",
        "theorem": "forall P Q : Prop, (P <-> Q) -> P -> Q"
    },

    9: {
        "title": "Disjunction Introduction",
        "statement": "Prove that if P is true, then P or Q is true.",
        "context": "",
        "theorem": "forall P Q : Prop, P -> P \\/ Q"
    },

    10: {
        "title": "Disjunction Elimination",
        "statement": "If P implies R and Q implies R, prove that P or Q implies R.",
        "context": "",
        "theorem": "forall P Q R : Prop, (P -> R) -> (Q -> R) -> P \\/ Q -> R"
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/problems")
def problem_list():
    return render_template(
        "problems.html",
        problems=problems
    )


@app.route("/problem/<int:problem_id>")
def problem(problem_id):

    current_problem = problems.get(problem_id)

    if current_problem is None:
        return "Problem not found", 404

    return render_template(
        "problem.html",
        problem=current_problem,
        problem_id=problem_id
    )


@app.route("/check-proof/<int:problem_id>", methods=["POST"])
def check_proof(problem_id):

    current_problem = problems.get(problem_id)

    if current_problem is None:
        return jsonify({
            "success": False,
            "message": "Problem not found."
        })

    data = request.get_json()
    user_proof = data["proof"]

    context = current_problem["context"]
    theorem = current_problem["theorem"]

    full_proof = f"""
{context}

Theorem problem : {theorem}.

Proof.

{user_proof}

Qed.
"""

    with open("temp_proof.v", "w") as file:
        file.write(full_proof)

    result = subprocess.run(
        ["rocq", "compile", "temp_proof.v"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return jsonify({
            "success": True,
            "message": "Proof accepted!"
        })

    return jsonify({
        "success": False,
        "message": result.stderr
    })


if __name__ == "__main__":
    app.run(debug=True)