import subprocess

proof = """
Theorem first_proof : forall P : Prop, P -> P.
Proof.
  intros P H.
  exact H.
Qed.
"""

with open("temp_proof.v", "w") as file:
    file.write(proof)

result = subprocess.run(
    ["rocq", "compile", "temp_proof.v"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Proof accepted")
else:
    print("Proof rejected")
    print(result.stderr)