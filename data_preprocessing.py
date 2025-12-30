import string
import re

punctuation = set(string.punctuation)
def data_cleaner_list(sentence):
  """
  To clean sentence by sentence as iterable:
    - lower casing
    - remove punctuation
    - remove numbers
    - remove multiple spaces
  """
  # In case of single sentence, transform it in a list/iterable
  if isinstance(sentence, str):
        sentence = [sentence]
  out_sen = []
  for sen in sentence:
    # lower casing
    sen = sen.lower()
    # removing punctuation
    for c in string.punctuation:
      sen = sen.replace(c, ' ')
    # remove numbers
    sen = re.sub(r"\d+", "", sen)
    # remove double spaces
    sen = re.sub(r"\s+", " ", sen)
    out_sen.append(sen)
  return out_sen