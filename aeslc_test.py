from datasets import load_dataset

dataset = load_dataset("aeslc")
print(dataset.keys())
print(dataset.values())
print(dataset['train']['email_body'][0:10])
print(dataset['validation']['subject_line'][0:10])
print(dataset['test']['subject_line'][0:10])
