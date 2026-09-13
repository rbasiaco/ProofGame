from flask import Flask, render_template, request, jsonify, redirect
import subprocess

app = Flask(__name__)


# -------------------------------------------------------------------
# PACKS
# -------------------------------------------------------------------

packs = {
    "foundations": {
        "title": "Foundations",
        "description": "Learn the basic logical structures and proof techniques used throughout mathematics.",
        "level": "Introductory"
    },

    "natural-numbers": {
        "title": "Natural Numbers",
        "description": "Explore arithmetic, induction, parity, and properties of the natural numbers.",
        "level": "Beginner"
    },

    "number-theory": {
        "title": "Number Theory",
        "description": "Work with divisibility, primes, greatest common divisors, and congruences.",
        "level": "Intermediate"
    },

    "analysis": {
        "title": "Analysis",
        "description": "Develop rigorous proofs involving inequalities, sequences, limits, and continuity.",
        "level": "Intermediate"
    },

    "geometry": {
        "title": "Geometry",
        "description": "Prove geometric results using formally defined objects and relationships.",
        "level": "Intermediate"
    }
}


# -------------------------------------------------------------------
# PROBLEMS
# -------------------------------------------------------------------

problems = {
    1: {
        "title": "Identity",
        "statement": "Prove that if P is true, then P is true.",
        "context": "",
        "theorem": "forall P : Prop, P -> P",
        "pack": "foundations"
    },

    2: {
        "title": "First Projection",
        "statement": "Prove that if P and Q are true, then P is true.",
        "context": "",
        "theorem": "forall P Q : Prop, P -> Q -> P",
        "pack": "foundations"
    },

    3: {
        "title": "Conjunction",
        "statement": "Prove that if P and Q are true, then P and Q are both true.",
        "context": "",
        "theorem": "forall P Q : Prop, P -> Q -> P /\\ Q",
        "pack": "foundations"
    },

    4: {
        "title": "Conjunction Elimination",
        "statement": "Prove that if P and Q are both true, then P is true.",
        "context": "",
        "theorem": "forall P Q : Prop, P /\\ Q -> P",
        "pack": "foundations"
    },

    5: {
        "title": "Implication Chaining",
        "statement": "If P implies Q and Q implies R, prove that P implies R.",
        "context": "",
        "theorem": "forall P Q R : Prop, (P -> Q) -> (Q -> R) -> P -> R",
        "pack": "foundations"
    },

    6: {
        "title": "Modus Tollens",
        "statement": "If P implies Q and Q is false, prove that P is false.",
        "context": "",
        "theorem": "forall P Q : Prop, (P -> Q) -> ~Q -> ~P",
        "pack": "foundations"
    },

    7: {
        "title": "Equivalence",
        "statement": "If P implies Q and Q implies P, prove that P and Q are logically equivalent.",
        "context": "",
        "theorem": "forall P Q : Prop, (P -> Q) -> (Q -> P) -> (P <-> Q)",
        "pack": "foundations"
    },

    8: {
        "title": "Using an Equivalence",
        "statement": "If P is logically equivalent to Q and P is true, prove that Q is true.",
        "context": "",
        "theorem": "forall P Q : Prop, (P <-> Q) -> P -> Q",
        "pack": "foundations"
    },

    9: {
        "title": "Disjunction Introduction",
        "statement": "Prove that if P is true, then P or Q is true.",
        "context": "",
        "theorem": "forall P Q : Prop, P -> P \\/ Q",
        "pack": "foundations"
    },

    10: {
        "title": "Disjunction Elimination",
        "statement": "If P implies R and Q implies R, prove that P or Q implies R.",
        "context": "",
        "theorem": "forall P Q R : Prop, (P -> R) -> (Q -> R) -> P \\/ Q -> R",
        "pack": "foundations"
    }
}


# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/packs")
def pack_list():
    return render_template(
        "packs.html",
        packs=packs,
        problems=problems
    )


# Keep old /problems links working
@app.route("/problems")
def old_problem_list():
    return redirect("/packs")


@app.route("/pack/<pack_id>")
def pack(pack_id):

    current_pack = packs.get(pack_id)

    if current_pack is None:
        return "Pack not found", 404

    pack_problems = {
        problem_id: problem
        for problem_id, problem in problems.items()
        if problem["pack"] == pack_id
    }

    return render_template(
        "pack.html",
        pack=current_pack,
        pack_id=pack_id,
        problems=pack_problems
    )


@app.route("/problem/<int:problem_id>")
def problem(problem_id):

    current_problem = problems.get(problem_id)

    if current_problem is None:
        return "Problem not found", 404

    current_pack = packs[current_problem["pack"]]

    return render_template(
        "problem.html",
        problem=current_problem,
        problem_id=problem_id,
        pack=current_pack,
        pack_id=current_problem["pack"]
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