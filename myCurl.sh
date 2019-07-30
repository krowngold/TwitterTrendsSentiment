curl -X POST      -H "Authorization: Bearer "$(gcloud auth application-default print-access-token)      -H "Content-Type: application/json; charset=utf-8"      --data "{
  'document':{
    'type':'PLAIN_TEXT',
    'content':'Michelangelo Caravaggio, Italian painter, is known for
              \'The Calling of Saint Matthew\'.'
  },
  'encodingType':'UTF8'
}" "https://language.googleapis.com/v1/documents:analyzeEntities"
