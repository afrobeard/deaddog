curl -X POST -u "9c811611-e318-401e-ad85-964540af0909":"mmuTs53xXOvV" \
--header "Content-Type: audio/wav" \
--data-binary @file.wav \
"https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?timestamps=true&word_alternatives_threshold=0.9"
