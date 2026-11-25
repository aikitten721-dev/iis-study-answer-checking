# Checking AI study answers against course notes

Prose word count: 384

## Project status

I developed a local application with Checking and Source retrieval views to explore how students check an AI explanation against its source. My three fixed examples cover supported wording, a qualification error and missing-source recovery. Browser controls handle feedback, rechecking, cancellation and reset. Semantic responses and keeping an explanation are simulated. Retrieval runs over eight sample documents. General claim comparison and persistent storage remain planned.

## Technology stack

I use Python 3.9+ and its standard library for the HTTP server and weighted word-overlap retriever, with HTML, CSS and JavaScript for the interface. The server loads case definitions from `fixtures.json` and resolves their passages from the same N1/N2 files indexed by retrieval. My corpus also includes six fictional handbook documents for source-version checks. Superseded passages receive a 0.3 score multiplier; scores express relative overlap within a query. No live model is connected yet; the choice of model for the planned comparator and the storage method for persistent notes remain undecided.

## Running and inspecting

```sh
python3 app.py
# Open http://127.0.0.1:8000
# Alternative port: python3 app.py --port 8004
python3 -m unittest discover -s tests -v
```

Start the server, open the application and follow each checking example. Use Cancel and Reset to inspect recovery. In Source retrieval, try the working-memory and recognition queries, then inspect the current/older-rule example and its ranking-adjustment notice. The project uses the Python standard library and local data.

## Development record

- Labs 1–2: I established the study-answer problem and developed evidence display and correction controls. In A1, I focused the question on omitted conditions and comparison with source links.
- Lab 3: I revised the qualification-error comparison and missing-source recovery path. Lab 4 added retrieval and source metadata and exposed an older handbook ranking first.
- Lab 5 and A2: I carried the superseded-source multiplier from the separate starter into the application, keeping older sources available for inspection.
- A2 consolidation: I added searchable N1/N2 notes, served fixtures from one endpoint and displayed the ranking adjustment. Eleven automated checks cover provenance, ranking, note consistency, case states and route responses; all pass.

## AI assistance

I led the research question, interaction design and project scope. I used ChatGPT to help generate interface and test boilerplate. I adapted the state transitions to my Lab design, requiring the old support label to be withdrawn before rechecking, and added missing-source and superseded-source cases. I also used ChatGPT to check the report for English grammar and clarity of expression.

## Additional files

My report accompanies the repository. All project materials needed for inspection are in this repository.
