# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.2] - 2024-01-20

### Changed

- Decoupling of state into different components.
- Evaluators renamed to Adaptors.


## [v0.0.1] - 2024-01-18

### Added

- Auto release to PyPI.

### Added

- A few implementations for baselines.

### Changed 

- Index now support batch size != 1 and k != 1.
- Batch size mandatary for Index, Embedders, LanguageModel, and Optimizer.
- Visualization change.

## [v0.0.0] - 2024-01-10

### Added

- Index - Faiss, Hnswlib, Polar, Whitening.
- Storage - Pandas, Datasets
- Embedders - SentenceTransformers
- Corpus - Composed
- LanguageModel - Huggingface
- Scores - BLEU (NLTK, SacreBLEU), Rouge (Rouge, RougeScore), Exact
- Adaptor - BigBench
- Optimizer - Ax / BoTorch, KMeans

[v0.0.1]: https://github.com/rentruewang/bocoel/compare/v0.0.0...v0.0.1
[v0.0.0]: https://github.com/rentruewang/bocoel/compare/v0.0.0
