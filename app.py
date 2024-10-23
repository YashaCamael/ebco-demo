from flask import Flask, request, jsonify
import os
import vertexai
import logging
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models


app = Flask(__name__)
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("GCP_REGION"))
model = GenerativeModel("gemini-1.0-pro-001")

def vertex_movie_recommendation(movies, scenario):
  try:
    response = model.generate_content(
      f"""You are an expert on box office movies. 
  Provide a recommendation for which of the following movies to watch: {" or ".join(movies)}
  where the scenario is: {scenario}""")
    return response.text

  except Exception as e:
    logging.exception(e)
    return "Unable to generate recommendation."

@app.route('/recommendations', methods=['POST'])
def movie_recommendations():
  """
  Returns movie recommendation based on the user's input.
  """
  if not request.json:
      return jsonify({'error': 'Missing JSON payload'}), 400
  movies = request.json['movies']
  scenario = request.json['scenario']
  recommendation_response = vertex_movie_recommendation(movies, scenario)
  return jsonify({'recommendation': recommendation_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)