import pandas as pd
import logging
import argparse
import logging
import os
from itertools import combinations
from dotenv import load_dotenv
from datetime import datetime
import openai
import anthropic
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, RetryError
from scipy.stats import pearsonr
from openai import OpenAIError
from pdme.evaluate import pdme_llm
from mistralai import Mistral, UserMessage
#from evaluate import pdme_llm

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
mistral_api_key = os.getenv('MISTRAL_API_KEY')
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.WARNING)
logging.getLogger("google.generativeai").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
from pdme.generate_bootstrap_prompts import create_bootstrap_prompts

# Function to load the markdown template
def load_template(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Template file not found: {file_path}")
        return ""

def load_questions(file_path):
    try:
        # Try to load the DataFrame from the specified Parquet file
        df = pd.read_parquet("hf://datasets/tatsu-lab/alpaca/data/train-00000-of-00001-a09b74b3ef9c3b56.parquet")
        logging.info(f"Loaded DataFrame from Parquet file with shape: {df.shape}")

        # Filter rows where 'input' is null or an empty string
        df_filtered = df[df['input'].isnull() | (df['input'] == '')].head(100)
        logging.info(f"Filtered DataFrame with null or empty 'input' and head 100: {df_filtered.shape}")

        # Extract questions from the 'instruction' column
        questions = df_filtered['instruction'].tolist()
        if questions:
            logging.info(f"Loaded questions from Parquet file. Total questions loaded: {len(questions)}")
        else:
            logging.error("No questions loaded from Parquet file.")
            questions = []
    except Exception as e:
        logging.error(f"Error loading Parquet file: {e}")
        questions = []

    # Fallback to loading the template if no questions are loaded
    if not questions:
        content = load_template(file_path)
        if content:
            questions = content.split('\n')
            questions = [q.strip() for q in questions if q.strip()]
            logging.info(f"Loaded questions from template. Total questions loaded: {len(questions)}")
        else:
            questions = []

    return questions

def generate_bootstrap_prompts(seeds, template, num):
    logging.info('Generating bootstrap prompts...')
    return create_bootstrap_prompts(template=template, seeds=seeds, num=num)

def generate_responses(model_name, question_prompts):
    logging.info('Generating responses using model %s...', model_name)
    responses = []

    if model_name.startswith("gpt"):
        client = openai.OpenAI(api_key=openai_api_key)
        completion_models = ["text-davinci-002", "text-davinci-003", "gpt-3.5-turbo-instruct"]
        is_completion = model_name in completion_models
        
        for item in question_prompts:
            try:
                if is_completion:
                    response = client.completions.create(
                        model=model_name,
                        prompt=item,
                        max_tokens=1000
                    )
                    responses.append(response.choices[0].text)
                else:
                    messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": item},
                    ]
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=1000
                    )
                    responses.append(response.choices[0].message.content)
            except Exception as e:
                logging.error(f"Error generating response for model %s: %s", model_name, e)
                responses.append(None)

    elif model_name.startswith("claude"):
        anthropic_client = anthropic.Client(api_key=anthropic_api_key)
        for item in question_prompts:
            try:
                response = anthropic_client.messages.create(
                    model=model_name,
                    max_tokens=1000,
                    messages=[
                        {"role": "user", "content": item}
                    ]
                )
                text_response = response.content[0].text
                responses.append(text_response)
            except Exception as e:
                logging.error(f"Error generating response for model %s: %s", model_name, e)
                responses.append(None)

    elif model_name.startswith("gemini"):
        genai.configure(api_key=google_api_key)
        model_last_part = model_name.split('/')[-1]
        logging.info('Generating for Gemini with: %s', model_last_part)
        model = genai.GenerativeModel(model_last_part)
        for item in question_prompts:
            try:
                response = model.generate_content(item)
                responses.append(response.text)
            except (GoogleAPICallError, RetryError, ValueError) as e:
                logging.error(f"Error generating response for model %s: %s", model_name, e)
                responses.append(None)

    elif model_name.startswith("mistral"):
        mistral_client = Mistral(api_key=mistral_api_key)
        for item in question_prompts:
            try:
                messages = [{"role": "user", "content": item}]
                chat_response = mistral_client.chat.complete(
                    model=model_name,
                    messages=messages,
                )
                responses.append(chat_response.choices[0].message.content)
            except Exception as e:
                logging.error(f"Error generating response for model %s: %s", model_name, e)
                responses.append(None)

    else:
        raise ValueError(f"Unsupported model name '{model_name}'.")

    return responses

def compute_correlations(df1, df2):
    try:
        # Dictionary mapping for creating the matching key
        model_mapping = {
            'gemini-1.5-pro-api-0514': 'gemini-1.5-pro',
            'gpt-4o-2024-05-13': 'gpt-4o',
            'gemini-1.5-pro-api-0409-preview': 'gemini-1.5-pro',
            'gpt-4-1106-preview': 'gpt-4',
            'gpt-3.5-turbo-0314': 'gpt-3.5-turbo'
        }

        # Apply mapping to create a match_key in df1
        df1['match_key'] = df1['model_name'].map(model_mapping)
        logging.debug(f"compute_correlations.df1 with match_key: {df1}")

        # Rename the columns for clarity before merging
        df2 = df2.rename(columns={'model_name': 'match_key'})

        # Merge DataFrames on the match_key
        merged_df = pd.merge(df1, df2, on='match_key')
        logging.info(f"compute_correlations.merged_df: {merged_df}")

        # Check the lengths before calculating correlation
        if len(merged_df) < 2:
            raise ValueError('The merged DataFrame must have at least 2 rows for correlation computation.')

        pearson_corr, pearson_p = pearsonr(merged_df['elo_ranking_x'], merged_df['elo_ranking_y'])
        
        return {
            "pearson_corr": pearson_corr,
            "pearson_p": pearson_p,
            "merged_df": merged_df
        }
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return {
            "pearson_corr": None,
            "pearson_p": None,
            "merged_df": None
        }

def save_battle_results(results_df, battles_output_file):
    try:
        now = datetime.now()
        timestamp = now.strftime("-%Y%m%d-%H%M")
        battles_output_file_with_timestamp = f"{battles_output_file.rstrip('.csv')}{timestamp}.csv"
        results_df.to_csv(battles_output_file_with_timestamp, index=False)
        logging.info(f"Results saved to {battles_output_file_with_timestamp}")
    except Exception as e:
        logging.error(f"Error saving results: %s", e)

def save_elo_rankings(elo_df, iter_elo_df, elo_output_file):
    try:
        now = datetime.now()
        timestamp = now.strftime("-%Y%mdd-%H%M")
        elo_output_file_with_timestamp = f"{elo_output_file.rstrip('.csv')}{timestamp}.csv"
        iter_elo_output_file_with_timestamp = f"{elo_output_file.rstrip('.csv')}{timestamp}-iter.csv"

        elo_df.to_csv(elo_output_file_with_timestamp, index=False)
        logging.info(f"Calibrated ELO rankings saved to %s", elo_output_file_with_timestamp)

        iter_elo_df.to_csv(iter_elo_output_file_with_timestamp, index=False)
        logging.info(f"Iterative ELO rankings saved to %s", iter_elo_output_file_with_timestamp)
    except Exception as e:
        logging.error(f"Error saving ELO rankings: %s", e)