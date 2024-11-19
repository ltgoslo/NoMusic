source ../pyenv/bin/activate

GOLD=../norsid_test.conll

echo "Baseline"
python ../scripts/sidEval.py $GOLD baseline/mbert_en.conll

echo "HITZ"
python ../scripts/sidEval.py $GOLD hitz/sid/sid1.conll
python ../scripts/sidEval.py $GOLD hitz/sid/sid2.conll
python ../scripts/sidEval.py $GOLD hitz/sid/sid3.conll

echo "MaiLAB"
python ../scripts/sidEval.py $GOLD mailab/mainlp_intents1_mdeberta_siddial_8446.conll
python ../scripts/sidEval.py $GOLD mailab/mainlp_intents2_mdeberta_topline_swapped.conll
python ../scripts/sidEval.py $GOLD mailab/mainlp_intents3_mdeberta_sidnor20_5678.conll
python ../scripts/sidEval.py $GOLD mailab/mainlp_slots1_mdeberta_siddial_8446.conll
python ../scripts/sidEval.py $GOLD mailab/mainlp_slots2_mdeberta_topline_swapped.conll
python ../scripts/sidEval.py $GOLD mailab/mainlp_slots3_scandibert_deprel_sid_8446.conll

echo "LTG"
python ../scripts/sidEval.py $GOLD ltg/nbbert_en.conll
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_nb.conll
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_nb_norsid.conll
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_nb_norsid_5epochs.conll
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_norsid.conll
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_norsid_11epochs.conll

echo "CUFE"
python ../scripts/sidEval.py $GOLD cufe/norsid_test_labels.conll

echo "LTG extra"
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_mas.conll
python ../scripts/sidEval.py $GOLD ltg/nbbert_en_mas_norsid.conll

echo "---------------"

echo "Baseline -- dialect"
python ../scripts/evalDialect.py $GOLD baseline/result_tfidf_svm_1-4gram.txt

echo "HITZ -- dialect"
python ../scripts/evalDialect.py $GOLD hitz/dialect/dialect1.conll
python ../scripts/evalDialect.py $GOLD hitz/dialect/dialect2.conll
python ../scripts/evalDialect.py $GOLD hitz/dialect/dialect3.conll

echo "CUFE"
python ../scripts/evalDialect.py $GOLD cufe/norsid_test_labels.conll

deactivate
