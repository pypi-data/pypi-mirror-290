import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from pdme.generate_bootstrap_prompts import create_bootstrap_prompts
from pdme.evaluate import pdme_llm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set logging level for external libraries to WARNING to suppress low-level logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)  # Suppress HTTP request logs if using requests library

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Function to load the markdown template
def load_template(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Template file not found: {file_path}")
        return ""
    
def generate_bootstrap_prompts(seeds, template, num):
    logging.info('Generating bootstrap prompts...')
    return create_bootstrap_prompts(template=template, seeds=seeds, num=num)

def generate_question_prompts(bootstrap_prompts, model_name, api_key):
    logging.info('Generating question prompts using model %s...', model_name)
    client = openai.OpenAI(api_key=api_key)
    question_prompts = []

    for item in bootstrap_prompts:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": item},
            ]
        )
        question_prompts.append(response.choices[0].message.content)
    
    return question_prompts

def generate_responses(model_name, question_prompts):
    logging.info('Generating responses using model %s...', model_name)
    responses = []

    if model_name.startswith("gpt"):
        client = openai.OpenAI(api_key=openai_api_key)
        for item in question_prompts:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": item},
                ]
            )
            responses.append(response.choices[0].message.content)

    elif model_name.startswith("claude"):
        anthropic_client = anthropic.Client(api_key=anthropic_api_key)
        for item in question_prompts:
            response = anthropic_client.messages.create(
                model=model_name,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": item}
                ]
            )
            text_response = response.content[0].text
            responses.append(text_response)

    else:
        huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not huggingface_api_key:
              raise ValueError("HuggingFace API key not found in environment variables.")
        login(huggingface_api_key)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        for item in question_prompts:
            inputs = tokenizer.encode(item, return_tensors="pt")
            outputs = model.generate(inputs, max_length=100)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            responses.append(response)

    return responses

def compare_responses(llm, prompt_1, prompt_2, labels):
        score_1 = llm.evaluate(prompt_1, labels)
        score_2 = llm.evaluate(prompt_2, labels)

        avg_scores = [(score_1[0] + score_2[1]) / 2, (score_1[1] + score_2[0]) / 2 ]
        print("avg_scores", avg_scores)
        return avg_scores

def score_responses(evaluation_prompt_template, question_prompts, responses_model_a, responses_model_b, client, eval_model):
    logging.info('Scoring responses...')
    llm = pdme_llm(client, eval_model)
    model_a_scores = []
    model_b_scores = []
    sum_model_a_scores = 0
    sum_model_b_scores = 0

    for i, question in enumerate(question_prompts):
        prompt_1 = evaluation_prompt_template.replace("<question_full>", question).replace("<response1>", responses_model_a[i]).replace("<response2>", responses_model_b[i])
        prompt_2 = evaluation_prompt_template.replace("<question_full>", question).replace("<response1>", responses_model_b[i]).replace("<response2>", responses_model_a[i])

        avg_score = compare_responses(llm, prompt_1, prompt_2, ["1", "2"])

        model_a_scores.append(avg_score[1])
        model_b_scores.append(avg_score[0])
        sum_model_a_scores += avg_score[1]
        sum_model_b_scores += avg_score[0]

    winner = "model_a" if sum_model_a_scores > sum_model_b_scores else "model_b"

    scores_dict = {
        "model_a_scores": model_a_scores,
        "model_b_scores": model_b_scores,
        "model_a_total_score": sum_model_a_scores,
        "model_b_total_score": sum_model_b_scores,
        "winner": winner
    }

    return scores_dict


def main(base_model, other_models, num_samples = 3):
    
    logging.info('Starting the main process with models %s...', other_models)
    logging.info('And base model %s', base_model)

    seeds = { 
        "<language>": ["python", "c++"],
        "<seed>": ["tic-tac-toe", "array", "sorting", "dictionary"],
    }

    bootstrap_prompt_template = """Write a question asking to make a programming challenge meant to evaluate programming abilities.
    The problem should be possible to solve in less than 100 lines of code for a very skilled programmer.
    The problem should use the <language> language, and be realted to these seeds: <seed>, <seed>."""

    bootstrap_prompts = generate_bootstrap_prompts(seeds, bootstrap_prompt_template, num=num_samples)

    for item in bootstrap_prompts:
        logging.info('Bootstrap prompt: %s', item)

    question_prompts = generate_question_prompts(bootstrap_prompts, model_name="gpt-3.5-turbo", api_key=openai_api_key)
    
    for item in question_prompts:
        logging.info('Question prompt: %s', item)

    results = []

    base_responses = generate_responses(base_model, question_prompts)

    model_responses = {}
    for item in other_models:
        responses = generate_responses(item, question_prompts)
        model_responses[item] = responses

    eval_model = "gpt-3.5-turbo-instruct"
    client = openai.OpenAI(api_key=openai_api_key)

    evaluation_prompt_template = load_template('templates/evaluation_template.md')

    all_scores = {}
    for i, item in enumerate(other_models):
        logging.info('Testing model %s', item)
        try:

            scores = score_responses(evaluation_prompt_template, question_prompts, base_responses, model_responses[item], client, eval_model)
            
            logging.info('Scores: %s', scores)
            all_scores[item] = scores["model_b_scores"]

        except Exception as e:
            logging.error('An error occurred during the testing of %s', item, e)
            continue

    # Rank models and save leaderboard
    logging.info('All models and scores %s', all_scores)
    logging.info('Base model %s, with score 0.5', base_model)

if __name__ == "__main__":
    base_model = 'gpt-4-turbo'
    model_list = ['gpt-4o', 'gpt-4', 'gpt-4-turbo']
    main(base_model, model_list)