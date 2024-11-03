import torch
from logical_utils.data_process_tools import *
from logical_utils.eval import *

class CodeToken:
    def __init__(self, data, tokenizer, model, model_name, candidates):
        self.original_tokens = data["truncate_tokens"]
        # print(self.original_tokens)
        self.intervention_tokens = self.original_tokens.copy()
        self.intervention_tokens = insert_not_before_last_in_list(self.intervention_tokens)
        # print(self.intervention_tokens)
        self.tokenizer = tokenizer
        self.model = model
        self.model_name = model_name
        self.candidates = candidates
        self.label = data["label"]

        '''
        if data["label"] == candidates[0]:
            self.label = [0]
        elif data["label"] == candidates[1]:
            self.label = [1]
        else:
            print("label error!!!")
        '''

        self.original_ids = tokenizer.convert_tokens_to_ids(self.original_tokens)
        self.intervention_ids = tokenizer.convert_tokens_to_ids(self.intervention_tokens)

        self.original_input = torch.tensor(self.original_ids)
        self.intervention_input = torch.tensor(self.intervention_ids)

        self.original_prob = self.get_prediction_probabilities(self.original_input)
        # print(self.original_prob)
        self.intervention_prob = self.get_prediction_probabilities(self.intervention_input)
        # print(self.intervention_prob)

    def calculate_effect(self):
        for c in self.original_prob:
            # print(c)
            # print(self.label)
            if c == self.label:
                self.original_odds = calculate_log_odds(self.original_prob[c])
                # print(self.original_odds)
                self.intervention_odds = calculate_log_odds(self.intervention_prob[c])
                # print(self.intervention_odds)
                self.odds_r = calculate_log_odds_r(self.original_prob[c],self.intervention_prob[c])
                #self.total_effect = total_effect(self.original_odds, self.intervention_odds)

    def get_prediction_probabilities(self, inputs):

        with torch.no_grad():
            self.outputs = self.model(inputs.unsqueeze(0), labels=inputs.unsqueeze(0))

        # obtain the logits of the last token
        self.logits = self.outputs.logits[:, -1, :]

        # using softmax to calculate prob distribution
        self.probs = torch.softmax(self.logits, dim=-1)

        # probs of each candidate words
        candidate_tokens = self.tokenizer.convert_tokens_to_ids(self.candidates)
        candidate_probs = self.probs[:, candidate_tokens].tolist()[0]

        word_probs = dict(zip(self.candidates, candidate_probs))
        return word_probs

    def code_to_dict(self):
        code_dict = {
            "original_tokens": self.original_tokens,
            "intervention_tokens": self.intervention_tokens,
            "model_name": self.model_name,
            "label": self.label,
            "original_ids": self.original_ids,
            "intervention_ids": self.intervention_ids,

            # "original_input" : self.original_input,
            # "intervention_input" : self.intervention_input,

            "original_prob": self.original_prob,
            "intervention_prob": self.intervention_prob,

            "original_odds": self.original_odds,
            "intervention_odds": self.intervention_odds,
            "odds_r": self.odds_r,
            #"total_effect": self.total_effect,
        }

        return code_dict


class CodeString:
    def __init__(self, data, tokenizer, model, model_name, candidates):
        self.original_string = data["truncate_code"]
        self.intervention_string = data["intervention_truncate_code"]

        self.label = data["label"]
        # print(f'# print(self.label) : {self.label}')
        self.tokenizer = tokenizer
        self.model = model
        self.model_name = model_name
        self.candidates = candidates

        self.original_input = self.tokenizer(self.original_string, return_tensors="pt")
        self.intervention_input = self.tokenizer(self.intervention_string, return_tensors="pt")

        self.original_prob, self.original_logits = self.get_prediction_probabilities(self.original_input)
        # print(f'# print(self.original_prob) : {self.original_prob}')
        self.intervention_prob, self.intervention_logits = self.get_prediction_probabilities(self.intervention_input)
        # print(f'# print(self.intervention_odds) : {self.intervention_prob}')

    def calculate_effect(self):
        for c in self.original_prob:
            # print(c)
            # print(self.label)
            if c == self.label:
                self.original_odds = calculate_log_odds(self.original_prob[c])
                # print(f'# print(self.original_odds) : {self.original_odds}')
                self.intervention_odds = calculate_log_odds(self.intervention_prob[c])
                # print(f'# print(self.intervention_odds) : {self.intervention_odds}')
                self.odds_r = calculate_log_odds_r(self.original_prob[c], self.intervention_prob[c])

                #self.total_effect = total_effect(self.original_odds, self.intervention_odds)
                # print(f'# print(self.total_effect) : {self.total_effect}')

    def get_prediction_probabilities(self, inputs):

        with torch.no_grad():
            self.outputs = self.model(**inputs, labels=inputs["input_ids"])

        # obtain the logits of the last token
        self.logits = self.outputs.logits[:, -1, :]

        # using softmax to calculate prob distribution
        self.probs = torch.softmax(self.logits, dim=-1)

        # probs of each candidate words
        candidate_tokens = self.tokenizer.convert_tokens_to_ids(self.candidates)
        candidate_probs = self.probs[:, candidate_tokens].tolist()[0]
        candidate_logits = self.logits[:, candidate_tokens].tolist()[0]

        word_probs = dict(zip(self.candidates, candidate_probs))
        word_logits = dict(zip(self.candidates, candidate_logits))
        return word_probs, word_logits

    def code_to_dict(self):
        code_dict = {
            "original_string": self.original_string,
            "intervention_string": self.intervention_string,
            "model_name": self.model_name,
            "label": self.label,
            "original_ids": self.original_input["input_ids"].tolist(),
            "intervention_ids": self.intervention_input["input_ids"].tolist(),

            # "original_input" : self.original_input,
            # "intervention_input" : self.intervention_input,

            "original_prob": self.original_prob,
            "intervention_prob": self.intervention_prob,
            "original_logits": self.original_logits,
            "intervention_logits": self.intervention_logits,
            "original_odds": self.original_odds,
            "intervention_odds": self.intervention_odds,
            "odds_r": self.odds_r,
            #"total_effect": self.total_effect
        }

        return code_dict
