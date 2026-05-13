from models.demo import predict, DIRECTORS, ACTORS, WRITERS
from flask import Flask, render_template, request
import json
app = Flask(__name__)

with open("../prediction/examples.json", "r", encoding="utf-8") as f:
    EXAMPLES = json.load(f)

ALL_DIRECTORS = sorted(DIRECTORS['director_name'].dropna().unique().tolist())
ALL_WRITERS = sorted(WRITERS['writer_name'].dropna().unique().tolist())
ALL_ACTORS = sorted(ACTORS['actor_name'].dropna().unique().tolist())
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
                "year": int(form_data['year']),
                "budget": int(form_data['budget']),
                "director": form_data['director'],
                "writer": form_data['writer'],
                "actors": [form_data[f'actor{i}'] for i in range(1, 6)]
            }
            prediction_result = predict(input_dict,model_path="../models/rf_best8.pickle").round(2)
        except Exception as e:
            prediction_result = f"Błąd: {str(e)}"

    return render_template('index.html',
                           prediction=prediction_result,
                           form_data=form_data,
                           examples=EXAMPLES,
                           selected_example=selected_example,
                           directors_list=ALL_DIRECTORS,
                           writers_list=ALL_WRITERS,
                           actors_list=ALL_ACTORS
                           )
if __name__ == '__main__':
    app.run(debug=True)