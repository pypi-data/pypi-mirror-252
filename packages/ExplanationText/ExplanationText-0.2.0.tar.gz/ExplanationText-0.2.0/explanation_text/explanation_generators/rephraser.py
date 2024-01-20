import re

from explanation_text.explanation_generators.api_utils import query_text_generation
from explanation_text.explanation_generators.explanation_generator_geoguesser.information_generator import remove_words_after_last_dot


def rephrase(mode, input_text, api_token, prompt=None):
    endpoint = "https://api-inference.huggingface.co/models/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}

    # estimate number of tokens in input text without actual tokenizer
    nr_input_tokens = int(len(re.findall(r'\w+', input_text)) * 1.3)

    # limit length of input to 4000 characters
    if len(input_text) > 4000:
        input_text = input_text[:4000]

    if prompt is None:
        prompt = (f"<|prompter|>Paraphrase the following text.\nOriginal: {input_text}\nParaphrase:<|endoftext"
                  f"|><|assistant|>")
    else:
        prompt = f"<|prompter|>{prompt}\nOriginal: {input_text}\nParaphrase:<|endoftext|><|assistant|>"

    if mode == "strict":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': nr_input_tokens, 'max_time': 60.0,
                         'num_beams': 3}
    elif mode == "variable":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': nr_input_tokens, 'max_time': 60.0,
                         'no_repeat_ngram_size': 3, 'num_beams': 5, 'do_sample': True,
                         'top_p': 0.95, 'temperature': 0.6}

    else:
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': nr_input_tokens, 'max_time': 60.0,
                         'no_repeat_ngram_size': 3, 'num_beams': 3, 'do_sample': True,
                         'top_p': 0.92, 'temperature': 0.6}

    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return remove_words_after_last_dot(return_text)

    print(return_text)
    return ""
