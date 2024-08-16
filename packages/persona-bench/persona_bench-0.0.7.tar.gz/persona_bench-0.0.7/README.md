<div align="center">


<p align="center"><h1 align="center">PERSONA Bench</h1>

<b>Reproducible Testbed for Evaluating and Improving Language Model Alignment with Diverse User Values</b>

<a href="https://www.synthlabs.ai/research/persona"><b>SynthLabs.ai/research/persona</b></a><br /><br />
<a href="https://www.synthlabs.ai"><img src="https://www.synthlabs.ai/img/persona.jpeg" alt="PERSONA" style="max-width: 100%;"></a><br /></p>


<p align="center">
<a href="https://github.com/SynthLabsAI/PERSONA-bench"><img src="https://img.shields.io/badge/GitHub-PERSONA--Bench-purple?logo=github" alt="GitHub Repository" style="max-width: 100%;"></a>
<a href="https://pypi.org/project/persona-bench/"><img src="https://badge.fury.io/py/persona-bench.svg" alt="PyPI version"/></a>
  <br/>
  <a href="https://www.synthlabs.ai/research/persona"><img src="https://img.shields.io/badge/docs-online-brightgreen" alt="Documentation" style="max-width: 100%;"></a>
  <a href="https://github.com/SynthLabsAI/PERSONA-bench/blob/main/CONTRIBUTING.md"><img src="https://img.shields.io/badge/Contributor-Guide-blue?logo=Github&color=purple" alt="Contributor Guide"/></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache-blue.svg" alt="License" style="max-width: 100%;"></a>
  <br/>
  <a href="https://arxiv.org/abs/2407.17387"><img src="https://img.shields.io/badge/arXiv-2407.17387-b31b1b.svg" alt="arXiv"/></a>
  <a href="https://www.synthlabs.ai/"><img src="https://img.shields.io/badge/AI-AI?labelColor=6466F1&color=D43B83&label=SynthLabs" alt="SynthLabs"/></a>
  <a href="https://ai.stanford.edu/"><img src="https://img.shields.io/badge/Stanford-AI%20Lab-D43B83?logo=stanford&logoColor=white" alt="Stanford AI Lab" style="max-width: 100%;"></a>
<a href="https://discord.gg/46uN42SE6x"><img src="https://img.shields.io/badge/Discord-Chat-blue?logo=discord&color=4338ca&labelColor=black" alt="Discord" style="max-width: 100%;"></a>
  <a href="https://twitter.com/synth_labs"><img src="https://img.shields.io/twitter/follow/synth_labs?style=social" alt="Twitter Follow" style="max-width: 100%;"></a>
</p>

[//]: # (  <a href="https://codecov.io/gh/SynthLabsAI/PERSONA-Bench"><img src="https://codecov.io/gh/SynthLabsAI/PERSONA-Bench/graph/badge.svg" alt="Coverage"/></a>)
[//]: # (<a href="https://github.com/SynthLabsAI/PERSONA-bench/actions/workflows/tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/SynthLabsAI/PERSONA-Bench/tests.yml?logo=githubactions&logoColor=white&label=Tests" alt="Tests" style="max-width: 100%;"></a>)

<p align="center">
  <a href="https://arxiv.org/abs/2407.17387">📄 Paper</a> |
  <a href="https://www.synthlabs.ai/research/persona">🗃️ Research Visualizations</a> |
  <a href="https://huggingface.co/SynthLabsAI">🤗 Hugging Face [Coming Soon]</a> |
  <a href="https://www.synthlabs.ai/research/persona">📚 Documentation</a>
</p>

<p align="center">
  <a href="https://www.synthlabs.ai/">🌐 SynthLabs Research</a> |
  <a href="https://jobs.synthlabs.ai/">👥 Join the Team</a> |
<a href="https://www.synthlabs.ai/contact">🤝 Let's Collaborate</a>
</p>

[//]: # ([![Tests]&#40;https://img.shields.io/github/actions/workflow/status/SynthLabs/PERSONA-bench/ci.yml?logo=github&label=Tests&#41;]&#40;https://github.com/SynthLabs/PERSONA-bench/actions&#41;)

</div>

PERSONA Bench is an extension of the PERSONA framework introduced in [Castricato et al. 2024](https://www.synthlabs.ai/research/persona). It provides a reproducible testbed for evaluating and improving the alignment of language models with diverse user values.
## Introduction

PERSONA established a strong correlation between human judges and language models in persona-based personalization tasks. Building on this foundation, we've developed a suite of robust evaluations to test a model's ability to perform personalization-related tasks. This repository provides practitioners with tools to assess and improve the pluralistic alignment of their language models.

Our evaluation suite uses [inspect-ai](https://inspect.ai-safety-institute.org.uk/) to perform various assessments on persona-based tasks, offering insights into model performance across different demographic intersections, feature importance, and personalization capabilities.

## Key Features

- 🎭 **Main Evaluation**: Assess personalized response generation
- 🧩 **Leave One Out Analysis**: Measure attribute impact on performance
- 🌐 **Intersectionality**: Evaluate model performance across different demographic intersections
- 🎯 **Pass@K**: Determine attempts needed for successful personalization

## Quick Start

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install the package:
   ```bash
   poetry add persona-bench
   ```

3. Use in your Python script:
   ```python
   from dotenv import load_dotenv
   from persona_bench import evaluate_model

   # optional, you can also pass the environment variables directly to evaluate_model
   load_dotenv()

   eval = evaluate_model("gpt-3.5-turbo", evaluation_type="main")
   print(eval.results.model_dump())
   ```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SynthLabs/PERSONA.git
   cd PERSONA
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

4. Set up HuggingFace authentication:
   ```bash
   huggingface-cli login
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   vim .env
   ```

## Detailed Evaluations

### Main Evaluation

The main evaluation script assesses a model's ability to generate personalized responses based on given personas from our custom filtered PRISM dataset.

<details>
<summary>Click to expand details</summary>

1. Load PRISM dataset
2. Generate utterances using target model with random personas
3. Evaluate using GPT-4 as a critic model via a debate approach
4. Analyze personalization effectiveness

</details>

### Leave One Out Analysis

This evaluation measures the impact of individual attributes on personalization performance.

<details>
<summary>Click to expand details</summary>

- Uses sub-personas separated by LOO attributes
- Tests on multiple personas and PRISM questions
- Analyzes feature importance

Available attributes include age, sex, race, education, employment status, and many more. See `example_LOO_JSON.json` for the full list.

</details>

### Intersectionality

Evaluate model performance across different demographic intersections.

<details>
<summary>Click to expand details</summary>

- Define intersections using JSON configuration
- Measure personalization across disjoint populations
- Analyze model performance for specific demographic combinations

</details>

### Pass@K

Determines how many attempts are required to successfully personalize for a given persona.

<details>
<summary>Click to expand details</summary>

- Reruns main evaluation K times
- Counts attempts needed for successful personalization
- Provides insights into model consistency and reliability

</details>

## Usage

Configure your `.env` file before running the scripts. You can set the generate mode to one of the following:
- `baseline`: Generate an answer directly, not given the persona
- `output_only`: Generate answer given the persona, without chain of thought
- `chain_of_thought`: Generate chain of thought before answering, given the persona
- `demographic_summary`: Generate a summary of the persona before answering

```bash
# Activate the poetry environment
poetry shell

# Main Evaluation
inspect eval src/persona_bench/main_evaluation.py --model {model}

# Leave One Out Analysis
inspect eval src/persona_bench/main_loo.py --model {model}

# Intersectionality Evaluation
inspect eval src/persona_bench/main_intersectionality.py --model {model}

# Pass@K Evaluation
inspect eval src/persona_bench/main_pass_at_k.py --model {model}
```

## Visualization

We provide scripts for visualizing evaluation results:

- `visualization_loo.py`: Leave One Out analysis
- `visualization_intersection.py`: Intersectionality evaluation
- `visualization_pass_at_k.py`: Pass@K evaluation

These scripts use the most recent log file by default. Use the `--log` parameter to specify a different log file.

## Dependencies

Key dependencies include:
- inspect-ai
- datasets
- pandas
- openai
- instructor
- seaborn

For development:
- tiktoken
- transformers

See `pyproject.toml` for a complete list of dependencies.

## Citation

If you use PERSONA in your research, please cite our paper:

```bibtex
@misc{castricato2024personareproducibletestbedpluralistic,
      title={PERSONA: A Reproducible Testbed for Pluralistic Alignment},
      author={Louis Castricato and Nathan Lile and Rafael Rafailov and Jan-Philipp Fränken and Chelsea Finn},
      year={2024},
      eprint={2407.17387},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.17387},
}
```

## Community & Support

Join our [Discord community](https://discord.gg/46uN42SE6x) for discussions, support, and updates or reach out to us at [https://www.synthlabs.ai/contact](https://www.synthlabs.ai/contact).

## Acknowledgements

This research is supported by SynthLabs. We thank our collaborators and the open-source community for their valuable contributions.

---

Copyright © 2024, [SynthLabs](https://www.SynthLabs.ai). Released under the Apache License.
