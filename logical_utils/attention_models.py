
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM


def get_model_tokenizer(model_name):
    if model_name == 0:
        model_n = "gpt2"
        # Load pre-trained model tokenizer (vocabulary)
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        # Load pre-trained model
        model = GPT2LMHeadModel.from_pretrained('gpt2', output_attentions=True,
                                                     output_hidden_states=True)
    elif model_name == 1:
        model_n = "codegemma"
        is_codegemma = True
        tokenizer = AutoTokenizer.from_pretrained("google/codegemma-2b")
        model = AutoModelForCausalLM.from_pretrained("google/codegemma-2b",
                                                          output_attentions=True,
                                                          output_hidden_states=True, 
                                                     attn_implementation="eager")
    elif model_name == 2:
        model_n = "codegen"
        is_codegen = True
        tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-2B-mono")
        model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-2B-mono",
                                                          output_attentions=True,
                                                          output_hidden_states=True)
    elif model_name == 3:
        model_n = "Phi"
        is_Phi = True
        tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True, output_attentions=True,
                                                          output_hidden_states=True)
    else:
        model_n = "gpt2"
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = GPT2LMHeadModel.from_pretrained('gpt2', output_attentions=True,
                                                     output_hidden_states=True)
    model.eval()
    return model, tokenizer, model_n