from models.demo import predict
from flask import Flask, render_template, request
import json
app = Flask(__name__)

with open("../prediction/examples.json", "r", encoding="utf-8") as f:
    EXAMPLES = json.load(f)
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_result = None
    form_data = {}

    selected_example = "custom"

    if request.method == 'POST':
        selected_example = request.form.get('example_choice')

        if selected_example and selected_example in EXAMPLES:
            form_data = EXAMPLES[selected_example]['data']
        else:
            form_data = request.form
            selected_example = "custom"

        try:

            input_dict = {
                "runtime": int(form_data['runtime']),
                "year": int(form_data['year']),
                "quarter": int(form_data['quarter']),
                "budget": int(form_data['budget']),
                "genres": [g.strip() for g in form_data['genres'].split(',')],
                "keywords": [k.strip() for k in form_data['keywords'].split(',')],
                "original_language": form_data['original_language'],
                "country": form_data['country'],
                "director": form_data['director'],
                "writer": form_data['writer'],
                "actors": [form_data[f'actor{i}'] for i in range(1, 6)]
            }
            prediction_result = predict(input_dict)
        except Exception as e:
            prediction_result = f"Błąd: {str(e)}"

    return render_template('index.html',
                           prediction=prediction_result,
                           form_data=form_data,
                           examples=EXAMPLES,
                           selected_example=selected_example)
if __name__ == '__main__':
    app.run(debug=True)