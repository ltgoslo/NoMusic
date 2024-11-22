# Norwegian slot and intent detection and dialect identification (NorSID)

## Participating teams

| Team   | Intents | Slots | Dialects |
|--------|---------|-------|----------|
| CUFE   | :heavy_check_mark:       |       | :heavy_check_mark:        |
| HITZ   | :heavy_check_mark:       | :heavy_check_mark:     | :heavy_check_mark:        |
| LTG    | :heavy_check_mark:       | :heavy_check_mark:     |          |
| MaiNLP | :heavy_check_mark:       | :heavy_check_mark:     |          |

## Intent detection

Dialect-specific and overall intent **accuracies**:

| Rank | System                              | B      | N      | T      | V      | Overall |
|------|-------------------------------------|--------|--------|--------|--------|---------|
| 1    | LTG 3 (nbbert_en_nb_norsid_5epochs) | 0.9800 | 0.9720 | 0.9827 | 0.9820 | 0.9802  |
| 2    | LTG 1 (nbbert_en_nb)                | 0.9820 | 0.9720 | 0.9833 | 0.9784 | 0.9789  |
| 3    | LTG 2 (nbbert_en_nb_norsid)         | 0.9820 | 0.9730 | 0.9813 | 0.9784 | 0.9785  |
| 4    | HITZ 2                              | 0.9820 | 0.9710 | 0.9760 | 0.9788 | 0.9769  |
| 5    | MaiNLP 3 (mdeberta_sidnor20_5678)   | 0.9780 | 0.9690 | 0.9800 | 0.9768 | 0.9764  |
| 6    | MaiNLP 2 (mdeberta_topline_swapped) | 0.9760 | 0.9620 | 0.9767 | 0.9716 | 0.9716  |
| 7    | HITZ 3                              | 0.9780 | 0.9540 | 0.9780 | 0.9724 | 0.9711  |
| 8    | HITZ 1                              | 0.9740 | 0.9540 | 0.9693 | 0.9604 | 0.9629  |
| 9    | CUFE 1                              | 0.9640 | 0.9330 | 0.9580 | 0.9356 | 0.9438  |
| 10   | MaiNLP 1 (mdeberta_siddial_8446)    | 0.9280 | 0.9260 | 0.9340 | 0.9400 | 0.9347  |
| 11   | Baseline (mBERT)                    | 0.8640 | 0.8260 | 0.8333 | 0.8480 | 0.8415  |

## Slot detection

Dialect-specific and overall **F1-scores**:

| Rank | System                                | B      | N      | T      | V      | Overall |
|------|---------------------------------------|--------|--------|--------|--------|---------|
| 1    | LTG 3 (nbbert_en_norsid_11_epochs)    | 0.9094 | 0.8719 | 0.8969 | 0.8949 | 0.8927  |
| 2    | LTG 2 (nbbert_en_norsid)              | 0.8992 | 0.8789 | 0.8927 | 0.8962 | 0.8925  |
| 3    | MaiNLP 2 (mdeberta_topline_swapped)   | 0.9011 | 0.7966 | 0.8518 | 0.8717 | 0.8557  |
| 4    | HITZ 1                                | 0.9109 | 0.7900 | 0.8548 | 0.8661 | 0.8537  |
| 5    | MaiNLP 1 (mdeberta_siddial_8446)      | 0.8560 | 0.8266 | 0.8299 | 0.8411 | 0.8368  |
| 6    | MaiNLP 3 (scandibert_deprel_sid_8446) | 0.8437 | 0.7925 | 0.8168 | 0.8401 | 0.8257  |
| 7    | LTG 1 (nbbert_en)                     | 0.8474 | 0.8009 | 0.8096 | 0.8330 | 0.8222  |
| 8    | HITZ 3                                | 0.7115 | 0.6098 | 0.6622 | 0.6818 | 0.6664  |
| 9    | Baseline (mBERT)                      | 0.7149 | 0.6068 | 0.6323 | 0.6505 | 0.6436  |
| 10   | HITZ 2                                | 0.5674 | 0.5194 | 0.5669 | 0.5625 | 0.5566  |

## Dialect detection

Dialect-specific and overall weighted **F1-scores**:

| Rank | System                | B      | N      | T      | V      | weighted |
|------|-----------------------|--------|--------|--------|--------|----------|
| 1    | HITZ 2                | 0.7540 | 0.7844 | 0.8595 | 0.8745 | 0.8417   |
| 2    | HITZ 3                | 0.7491 | 0.7750 | 0.8429 | 0.8708 | 0.8332   |
| 3    | HITZ 1                | 0.7410 | 0.7572 | 0.8397 | 0.8661 | 0.8271   |
| 4    | CUFE                  | 0.6893 | 0.7338 | 0.8026 | 0.8414 | 0.7964   |
| 5    | Baseline (TF-IDF SVM) | 0.5738 | 0.7346 | 0.7776 | 0.8259 | 0.7742   |
