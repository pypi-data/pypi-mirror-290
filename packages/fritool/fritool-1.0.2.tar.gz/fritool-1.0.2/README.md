# fritool

Python toolkit for calculating the Financial Resilience Institute's (FRI) personal resillience scores using FRI's API endpoints and the current index scoring model. For more information, please see https://financialresiliencescore.com

## Installation

Install package using pypi

```python
pip install fritool
```

Pypi project page https://pypi.org/project/fritool/

## Initializing the API Client

```python
from fritool.apiclient import ApiClient
apiclient = ApiClient(api_key="demokey")
```

API access is currently open to the public for testing and noncommercial use only. To obtain non-public API key and for licensing information please contact info@finresilienceinstitute.org

## Building the Questionnaire

Collect the list of questions that make up the currnet Institute's Financial Resillience Questionnaire:

```python
questions = apiclient.collect_questions()
```

The result is a list of all questions along with available answer options, with each question formatted as a separate dictionary. For example:

```console
{'id': '1',
  'question': 'Overall, how confident are you that you can get through periods of financial hardship resulting from unplanned events?',
  'answers': [{'text': '1', 'value': 1},
   {'text': '2', 'value': 2},
   {'text': '3', 'value': 3},
   {'text': '4', 'value': 4},
   {'text': '5', 'value': 5},
   {'text': '6', 'value': 6},
   {'text': '7', 'value': 7},
   {'text': '8', 'value': 8},
   {'text': '9', 'value': 9},
   {'text': '10', 'value': 10}],
  'type': 'confidence',
  'extents': ['1 - Not at all confident', '10 - Extremely confident'],
  'title': 'Overall, how confident are you that you can get through periods of financial hardship resulting from unplanned events?',
  'isFirst': True}
```

## Formatting the Answers

Format answers as a dictionary using question id as dictionary keys. For example:

```console
{0: {'answer': '10',
  'question': 'Overall, how confident are you that you can get through periods of financial hardship resulting from unplanned events?'}}
```

For testing purposes, generate a dictionary containing random answers to all of the questions in questionnaire as follows:

```console
answers = apiclient.generate_mock_answers(questions)
```

## Scoring and Interpreting Financial Resilience Scores

Score the answers using calculate_score() method:

```python
scores = apiclient.calculate_score(answers)
```

Scores will be a dictionary containing financial resilience scores for the questionnaire:

```console
{'index_score': 42,
 'index_score_value_to_compare': 32.87,
 'index_score_result': 28}
```
Where index_score is the final Resilience Score, index_score_value_to_compare is the mean Resilience Score value for all Canadians whom the Financial Resilience Institute polls and serves as the baseline for comparison, and index_score_result is the percentage difference between final index score and this mean value.

## Complete Example

```python
from fritool.apiclient import ApiClient

apiclient = ApiClient(api_key="demokey")
questions = apiclient.collect_questions()
answers = apiclient.generate_mock_answers(questions)
scores = apiclient.calculate_score(answers)

if scores['index_score_result'] > 0:
    print(f"Your score is {scores['index_score']} which is {scores['index_score_result']}% higher than the average score {scores['index_score_value_to_compare']}")
else:
    print(f"Your score is {scores['index_score']} which is {abs(scores['index_score_result'])}% lower than the average score {scores['index_score_value_to_compare']}")
