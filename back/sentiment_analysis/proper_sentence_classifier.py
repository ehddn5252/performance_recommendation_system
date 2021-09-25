from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F

device = torch.device('cpu')

def tokenize(text, tokenizer):
    all_input_ids = []
    all_input_mask = []
    tokens = tokenizer.tokenize(text)

    # limit size to make room for special tokens
    if MAX_SEQ_LEN:
        tokens = tokens[0:(MAX_SEQ_LEN - 2)]

    # add special tokens
    tokens = [tokenizer.cls_token, *tokens, tokenizer.sep_token]

    # convert tokens to IDs
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    # create mask same size of input
    input_mask = [1] * len(input_ids)

    all_input_ids.append(input_ids)
    all_input_mask.append(input_mask)

    # pad up to max length
    # up to max_seq_len if provided, otherwise the max of current batch
    max_length = MAX_SEQ_LEN if MAX_SEQ_LEN else max([len(ids) for ids in all_input_ids])

    all_input_ids = torch.LongTensor([i + [tokenizer.pad_token_id] * (max_length - len(i))
                                      for i in all_input_ids])
    all_input_mask = torch.FloatTensor([m + [0] * (max_length - len(m)) for m in all_input_mask])

    return all_input_ids, all_input_mask

count = 0
final_result = []
model_name = "Bert-Medium"
count += 1
MAX_SEQ_LEN = 512
#from glob import glob
#folders = glob(r"C:\Users\dw\github_repository\KOPIS_big_data_analysis\sentiment_analysis\sentiment_analysis\save_model\*")
#print(folders)

folder_name = r"./sentiment_analysis/kcbert-base-badSentence_naver_shopping_model.state(epoch7-0.9545)"
if "kcbert" in folder_name:
    MAX_SEQ_LEN = 300

print("folder_name is ")
print(folder_name)
tokenizer = BertTokenizer.from_pretrained(folder_name)
model = BertForSequenceClassification.from_pretrained(folder_name)
model = model.to(device)
model = model.eval()

def sentiment_analysis(text : str) -> str:
    input_ids, attention_mask = tokenize(text, tokenizer)
    outputs = model(input_ids = input_ids.to(device),
                    attention_mask=attention_mask.to(device))
    predict_content = outputs.logits.argmax(axis=-1).flatten().tolist()[0]
    
    return predict_content

    if predict_content == 0:
        return "negative"
    elif predict_content == 1:
        return "positive"