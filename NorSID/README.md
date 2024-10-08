# Norwegian slot and intent detection and dialect identification (NorSID)

Shared task website: https://sites.google.com/view/vardial-2025/shared-tasks

## Development data

The development data can be found in `norsid_dev.conll`.

Example:

```
# id = 33/8
# text = Kor varmt skal det ver i dag?
# intent = weather/find
# dialect = V
1   Kor     weather/find   O
2   varmt   weather/find   B-weather/attribute
3   skal    weather/find   O
4   det     weather/find   O
5   ver     weather/find   O
6   i       weather/find   B-datetime
7   dag     weather/find   I-datetime
8   ?       weather/find   O
```

- The `id` field contains the sentence id (`33`) and the translator id (`8`), separated by `/`.
  - Sentence ids range from 1 to 300 in the development set. All sentences with the same id are translations of each other, i.e. sentence 78/1 is just another dialectal variant of sentence 78/2.
  - Translator ids range from 1 to 10 as well as B (Bokmål).
- The `text` field represents the detokenized prompt string.
- The `intent` field contains the name of the intent associated with the prompt.
  - Some intent labels contain `/` but others don't.
- The `dialect` field contains the dialect label (one uppercase character).
  - There are four dialect labels: `V, N, T, B` (see Table below for details).
- The numbered lines contain the tokens of the prompt, together with the intent label and the slot annotations.
  - Some slot labels contain `/` but others don't (e.g. `weather/attribute` vs. `datetime`).

The correspondences between dialect areas and translator ids are as follows:

| Translator ID  | Origin | Dialect area |
| --- | ----------- | ------------- |
| 1  | Trondheim    | `T` (Trøndersk)       |
| 2  | Trondheim    | `T` (Trøndersk)       |
| 3  | Tromsø       | `N` (North Norwegian) |
| 4  | Haugesund    | `V` (West Norwegian)  |
| 5  | Sunndal      | `T` (Trøndersk)       |
| 6  | Tromsø area  | `N` (North Norwegian) |
| 7  | Ålesund area | `V` (West Norwegian)  |
| 8  | Stavanger    | `V` (West Norwegian)  |
| 9  | Stavanger    | `V` (West Norwegian)  |
| 10 | Bergen       | `V` (West Norwegian)  |
| B  |              | `B` (Bokmål)          |

## Test data

The test set is expected to be released on 4 November 2024. The test set will only contain the tokenized and untokenized prompt strings.
