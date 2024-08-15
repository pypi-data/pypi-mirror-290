import argparse
import logging
import os
import pandas as pd
from itertools import combinations
from dotenv import load_dotenv
import openai
from openai import OpenAIError
from pdme.evaluate import pdme_llm
from utils import generate_bootstrap_prompts, generate_responses, load_template, save_battle_results, save_elo_rankings, compute_correlations, load_questions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.WARNING)
logging.getLogger("google.generativeai").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

def generate_question_prompts(bootstrap_prompts, model_name, api_key):
    logging.info('Generating question prompts using model %s...', model_name)
    client = openai.OpenAI(api_key=api_key)
    question_prompts = []

    for item in bootstrap_prompts:
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": item},
            ]
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            question_prompts.append(response.choices[0].message.content)
        except Exception as e:
            logging.error(f"Error generating question prompt for model %s: %s", model_name, e)
    
    return question_prompts

def compare_responses(llm, prompt_1, prompt_2, labels):
    score_1 = llm.evaluate(prompt_1, labels)
    score_2 = llm.evaluate(prompt_2, labels)

    avg_scores = [(score_1[0] + score_2[1]) / 2, (score_1[1] + score_2[0]) / 2]
    logging.info("avg_scores %s", avg_scores)
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

def evaluate_models(model_pairs, question_prompts, evaluation_prompt_template, client, eval_model, base_model, num_prompts, eval_type):
    battles_df = pd.DataFrame(columns=["model_a", "model_b", "model_a_scores", "model_b_scores", "model_a_total_score", "model_b_total_score", "winner", "run_type"])
    run_type = f"base_{num_prompts}_{eval_type}"
    
    for model_a, model_b in model_pairs:
        logging.info(f'Generating responses for model_a: {model_a} and model_b: {model_b}')
        
        try:
            responses_model_a = generate_responses(model_a, question_prompts)
            if responses_model_a is None:
                logging.warning(f'Skipping evaluation for model_a: {model_a} due to generation error.')
                continue
        except OpenAIError as e:
            logging.error(f"OpenAI error generating responses for %s: %s", model_a, e)
            continue
        except Exception as e:
            logging.error(f"Unexpected error generating responses for %s: %s", model_a, e)
            continue

        try:
            responses_model_b = generate_responses(model_b, question_prompts)
            if responses_model_b is None:
                logging.warning(f'Skipping evaluation for model_b: {model_b} due to generation error.')
                continue
        except OpenAIError as e:
            logging.error(f"OpenAI error generating responses for %s: %s", model_b, e)
            continue
        except Exception as e:
            logging.error(f"Unexpected error generating responses for %s: %s", model_b, e)
            continue
        
        scores = score_responses(evaluation_prompt_template, question_prompts, responses_model_a, responses_model_b, client, eval_model)

        logging.info(f'evaluate_models: scores: {scores}')
        winner = scores["winner"]
        
        new_row = pd.DataFrame({
            "model_a": [model_a],
            "model_b": [model_b],
            "model_a_scores": [scores["model_a_scores"]],
            "model_b_scores": [scores["model_b_scores"]],
            "model_a_total_score": [scores["model_a_total_score"]],
            "model_b_total_score": [scores["model_b_total_score"]],
            "winner": [winner],
            "run_type": [run_type]
        })

        battles_df = pd.concat([battles_df, new_row], ignore_index=True)
        logging.info(battles_df)

    return battles_df

def setup_prompts(eval_type, num_prompts, openai_api_key):
    if eval_type in ['coding', 'story_telling']:
        if eval_type == 'coding':
            seeds = { 
                "<language>": ["python", "c++"],
                "<seed>": ["tic-tac-toe", "array", "sorting", "dictionary"],
            }
            bootstrap_prompt_template = load_template('templates/coding_template.md')
        elif eval_type == 'story_telling':
            seeds = {
                "seed_1": ["a haunted house", "a time traveler", "a magical forest"],
                "seed_2": ["redemption", "discovery", "loss"],
                "seed_3": ["a talking animal", "an ancient artifact", "a secret society"],
                "seed_4": ["a plot twist", "a moral dilemma", "an unexpected friendship"]
            }
            bootstrap_prompt_template = load_template('templates/story_telling_template.md')

        bootstrap_prompts = generate_bootstrap_prompts(seeds, bootstrap_prompt_template, num=num_prompts)
        question_prompts = generate_question_prompts(bootstrap_prompts, model_name="gpt-3.5-turbo", api_key=openai_api_key)

    elif eval_type == 'generic':
        general_questions_file_path = 'templates/general_question_template.md'
        all_questions = load_questions(general_questions_file_path)
        question_prompts = all_questions[:num_prompts]

    return question_prompts

def generate_model_pairs(model_list, eval_model, base_model, battle_type):
    if base_model in model_list:
        model_list = [model for model in model_list if model != base_model]

    if battle_type == "all":
        return list(combinations(model_list, 2))
    elif battle_type == "base":
        return [(base_model, model) for model in model_list if model != eval_model]
    else:
        raise ValueError(f"Unsupported battle type '{battle_type}'.")
    
def main(models_file, eval_type, num_prompts, battles_output_file, elo_output_file, elo_calibration_model, elo_benchmark_file, eval_model, base_model, battle_type):
    # Load models from CSV file
    models_df = pd.read_csv(models_file)
    model_list = models_df['model_name'].tolist()

    # Generate model pairs based on the battle type
    model_pairs = generate_model_pairs(model_list, eval_model, base_model, battle_type)

    # Set up prompts
    question_prompts = setup_prompts(eval_type, num_prompts, openai_api_key)

    if not question_prompts:
        logging.error("No question prompts generated. Exiting.")
        return

    # Load evaluation model and client
    client = openai.OpenAI(api_key=openai_api_key)
    evaluation_prompt_template = load_template('templates/evaluation_template.md')

    # Evaluate models
    battles_df = evaluate_models(model_pairs, question_prompts, evaluation_prompt_template, client, eval_model, base_model, num_prompts, eval_type)

    # Modify battles_output_file to include battle_type
    battles_output_file_with_type = battles_output_file.replace(".csv", f"_{battle_type}_{eval_type}_{num_prompts}.csv")

    # Save results
    logging.info(f'Saving battle results to {battles_output_file_with_type}')
    save_battle_results(battles_df, battles_output_file_with_type)

    # Compute benchmarked ELO rankings
    elo_output_file_with_type = elo_output_file.replace(".csv", f"_{battle_type}_{eval_type}_{num_prompts}.csv")
    elo_df = pdme_llm.compute_online_elo(battles_df, elo_calibration_model)
    iter_elo_df = pdme_llm.calculate_elo_iterative(battles_df)
    save_elo_rankings(elo_df, iter_elo_df, elo_output_file_with_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PDME Arena evaluation.")
    parser.add_argument("--models_file", type=str, required=True, help="Path to the CSV file containing model names.")
    parser.add_argument("--eval_type", type=str, choices=["generic", "coding", "story_telling"], required=True, help="Type of evaluation.")
    parser.add_argument("--num_prompts", type=int, default=5, help="Number of prompts to generate.")
    parser.add_argument("--battles_output_file", type=str, default="data/generic_battles.csv", help="Path to the output CSV file for battle results.")
    parser.add_argument("--elo_output_file", type=str, default="data/generic_elo.csv", help="Path to the output CSV file for elo rankings.")
    parser.add_argument("--elo_calibration_model", type=str, default="claude-3-opus-20240229", help="ELO calibration model.")
    parser.add_argument("--elo_benchmark_file", type=str, default="data/llmarena_elo.csv", help="ELO benchmark file to correlate to.")
    parser.add_argument("--eval_model", type=str, default="gpt-3.5-turbo-instruct", help="Evaluation model.")
    parser.add_argument("--base_model", type=str, default="gpt-4o", required=True, help="Base model for base_to_all battles.")
    parser.add_argument("--battle_type", type=str, default="base", choices=["all", "base"], required=True, help="Type of battle.")
    args = parser.parse_args()
    main(args.models_file, args.eval_type, 
         args.num_prompts, args.battles_output_file, 
         args.elo_output_file, 
         args.elo_calibration_model, args.elo_benchmark_file,
         args.eval_model, args.base_model, args.battle_type)