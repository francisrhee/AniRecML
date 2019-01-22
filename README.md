# AniRecML
A machine learning-based recommendation system for upcoming anime series, using the AniList API.

This was a project just for fun - I was curious about how machine learning could be implemented, and I also wanted some new shows to watch.

I tried 2 different approaches: collaborative filtering and content-based algorithms. I learned that most other recommendation systems use collaborative filtering unless they have the necessary metadata (ie. features) for the entries. The API did not provide adequate metadata, so I dropped the content-based approach and proceeded with the collaborative filtering approach instead. The code can be found in `/src/collabfilt`.

AniList API: https://github.com/AniList/ApiV2-GraphQL-Docs  
Surprise: http://surpriselib.com/

## Analysis
I wanted to know about the efficiencies of various algorithms provided in the library, so I did some analysis using sample data (1000 users).

The following results are average metrics over 3 trials, featuring both memory-based (KNN) and model-based algorithms.

| Algorithm	| Biased RMSE	| Unbiased RMSE	| Fit time (s)	| Test time (s)	| F1 Score |
| --- | --- | --- | --- | --- | --- |
| KNN (k=40)	| 1.1345	| 1.5419	| 1.05	| 14.78	| 0.72537984110245405 |
| KNN (k=80)	| 1.1366	| 1.5321	| 0.85	| 13.98	| 0.7277026513308035 |
| SVD	| 1.1173	| 1.3990	| 4.00	| 1.090	| 0.7230431884057591 |
| Slope One	| 1.1556	| 2.8125	| 3.63	| 21.53	| 0.71215194068146635 | 
| Co-clustering	| 1.3277	| 1.4289	| 5.26	| 1.000	| 0.71976771295736115 |
