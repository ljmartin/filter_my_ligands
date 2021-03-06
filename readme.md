# Filter my ligands

This is a readme


To-do:
MVP: 
- [x] make a to-do list
- [x] make a minimal dataframe - a few chemicals and ranking scores
- [x] make a minimal notebook that just loads the data
- [x] write a YAML file for binder
- [x] run and display ligands in binder

Pre-Alpha:
- [x] implement "landing page" i.e. some text in a notebook (streamlit?) that describes the project and gives instructions
- [x] ability to read user-uploaded CSV files
- [x] fingerprint
- [x] clustering options - HDSCAN, k-means, fastcluster? PARIS? 
- [x] display top N clusters interactively 
- [x] calculate QED score
- [ ] calculate various tox. filters
- [x] fold QED, tox into a dataframe
- [ ] display QED and tox filter limits interactively
- [ ] calculate similarity to existing ligands, performed within notebook or separately? may need flexible interpretation of the CSV so the user can input their own filtration data. 
- [ ] output data?? may have to be run locally, with a test version available on binder. 
- [ ] some unit tests

Beta:
- [ ] tidy up landing page. 
- [ ] email or save data to user's github.
- [ ] run with a PPAR gamma (or other well known target) dataset
- [ ] error handling. How to handle ranking ties? What about SMILES filtering or kekulization errors? empty columns? uninterpretable columns? accidental commas or tabs?


