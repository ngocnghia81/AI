from flask import Flask, render_template, request

app = Flask(__name__)

# Danh sách các bệnh và triệu chứng
class Disease:
    def __init__(self, name, symptoms):
        self.name = name
        self.symptoms = symptoms

# Tạo danh sách các bệnh với triệu chứng
diseases = [
    Disease("Cúm", ["sốt", "ho", "đau đầu"]),
    Disease("Viêm họng", ["đau họng", "khó nuốt", "sốt"]),
    Disease("Viêm phổi", ["ho", "khó thở", "sốt"]),
    Disease("COVID-19", ["sốt", "ho", "mất vị giác"]),
    Disease("Dị ứng", ["hắt hơi", "ngứa"]),
]

def are_complementary(lit1, lit2):
    if lit1.startswith('không '):
        return lit2 == lit1[6:]  # So sánh lit2 với lit1 không có tiền tố
    elif lit2.startswith('không '):
        return lit1 == lit2[6:]  # So sánh lit1 với lit2 không có tiền tố
    return False  # Không phải là mâu thuẫn

def resolve(clause1, clause2):
    resolvents = []
    for lit1 in clause1:
        for lit2 in clause2:
            if are_complementary(lit1, lit2):
                new_clause = list(set(clause1) | set(clause2) - {lit1, lit2})
                resolvents.append(new_clause)

                if is_empty_clause(new_clause):
                    return [new_clause]  # Trả về danh sách chứa mệnh đề rỗng
    return resolvents

def is_empty_clause(clause):
    return len(clause) == 0

def robinson_algorithm(clauses):
    steps = []
    new = set()
    existing_clauses = set(tuple(clause) for clause in clauses)

    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]

        for (clause1, clause2) in pairs:
            resolvents = resolve(clause1, clause2)
            for res in resolvents:
                if is_empty_clause(res):
                    steps.append({
                        'clause1': clause1,
                        'clause2': clause2,
                        'resolvent': res,
                        'is_empty': True
                    })
                    return steps, True
                new.add(tuple(res))
                steps.append({
                    'clause1': clause1,
                    'clause2': clause2,
                    'resolvent': res,
                    'is_empty': False
                })

        if new.issubset(existing_clauses):
            return steps, False

        existing_clauses.update(new)
        clauses.extend(list(new))

def diagnose(symptoms):
    possible_diseases = []

    for disease in diseases:
        clause = []
        for symptom in disease.symptoms:
            if symptom in symptoms:
                clause.append(symptom)  # Triệu chứng khớp
            else:
                clause.append(f'không {symptom}')  # Triệu chứng không khớp

        possible_diseases.append((disease.name, clause))

    return possible_diseases

# Route hiển thị trang chính và nhập triệu chứng
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symptoms_input = request.form.get("symptoms")
        symptoms = [symptom.strip().lower() for symptom in symptoms_input.split(",")]

        possible_diseases = diagnose(symptoms)
        clauses = [clause for _, clause in possible_diseases]

        steps, result = robinson_algorithm(clauses)

        return render_template("result.html", steps=steps, result=result, diseases=possible_diseases)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
