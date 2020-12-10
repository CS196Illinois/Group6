from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

class Summarizer:
  def __init__(self, model_name_or_path, device='cpu'):
    self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path)
    self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    self.pipeline = pipeline('summarization', model=self.model, tokenizer=self.tokenizer)
    self.model = self.model.to(device)

  def summarize(self, text, length):
    return self.pipeline(text, min_length=1, max_length=length)[0]['summary_text']

