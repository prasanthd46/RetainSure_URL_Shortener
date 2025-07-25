>> Design Notes : 

Thread Safety -->  All write operations on the store (saving, incrementing clicks) are protected by a threading.Lock to handle concurrency.

Idempotency --> Same URL always returns the same short code using url_to_code reverse lookup map.

Short Code Generation --> Random alphanumeric codes of length 6 are generated uniquely against existing codes.

Error Handling --> All HTTP errors are returned in consistent JSON format using flasks http handler.

Testing --> 9 tests written with pytest to cover edgecases and normal functionality.

Blueprints --> Used Blueprint to keep route logic modular and also clean.


>> Implementation Things : 

Short Code Generation -->  Generates a unique 6-character alphanumeric code for each URL( repeated URLs always get the same code ).

URL Validation --> Uses regex to ensure the URL is valid and includes a public domain (not just any string).

Data Storage --> Uses two dicts in UrlStore for O(1) lookup in retrieving url and idempotency for repeated shortens.

>> About AI Usage : 

I Used perplexity to refer for some production level code desicions and improvements in things like validation, in-memory store.
By using AI coding assistants for structure, code reviews, and validation regex improvements. Final code was verified and adapted by me to fit assignment requirements and test coverage.

>> Also Used for : 

   > Understanding the need for dual mappings

   > Suggesting concise URL validation regex.
   
   > Improving errorhandler for consistent JSON responses.