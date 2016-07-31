curl -i -u "f7b80c7f-f38c-48ba-b9aa-df084b18aad3":"wDMumbSiYyND" \
-F training_data=@watson-training-data.csv \
-F training_metadata="{\"language\":\"en\",\"name\":\"GovHackClassifier\"}" \
"https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"



