import asyncio
import os
from typing import Literal

from inspect_ai._eval.eval import eval_async
from inspect_ai.log import EvalLog

from persona_bench.main_evaluation import persona_bench_main as eval_main
from persona_bench.main_intersectionality import (
    persona_bench_intersectionality as eval_intersectionality,
)
from persona_bench.main_loo import persona_bench_loo as eval_loo
from persona_bench.main_pass_at_k import persona_bench_pass_at_k as eval_pass_at_k

_env = os.getenv


async def async_evaluate_model(
    model_str: str,
    evaluation_type: Literal["main", "loo", "intersectionality", "pass_at_k"] = "main",
    log_dir: str = "/tmp/",
    seed: int = None,
    N: int = None,
    OPENAI_API_KEY: str = _env("OPENAI_API_KEY"),
    GENERATE_MODE: Literal[
        "baseline", "output_only", "chain_of_thought", "demographic_summary"
    ] = _env("GENERATE_MODE"),
    INTERSECTION_JSON: str = _env("INTERSECTION_JSON"),
    LOO_JSON: str = _env("LOO_JSON"),
    INSPECT_EVAL_MODEL: str = _env("INSPECT_EVAL_MODEL"),
) -> asyncio.Future:
    """
    Async. runs persona bench over the model specified by model_str

    Args:
        model_str (str): The model to evaluate
        evaluation_type (Literal["main", "loo", "intersectionality", "pass_at_k"], optional): The evaluation type to run. Defaults to "main".
        log_dir (str, optional): The directory to store the logs. Defaults to "/tmp/".
        seed (int, optional): The seed to use for the evaluation. Defaults to None.
        N (int, optional): The number of samples to use for the evaluation. Defaults to None (all samples).
        OPENAI_API_KEY (str, optional): The openai used for rewriting the model output to be pydantic compliant. Defaults to env("OPENAI_API_KEY").
        GENERATE_MODE (Literal["baseline", "output_only", "chain_of_thought", "demographic_summary"], optional): The mode to use for generating the prompts. Defaults to env("GENERATE_MODE").
        INTERSECTION_JSON (str, optional): The intersectionality json file. Defaults to env("INTERSECTION_JSON"). See the readme on how to set this file up.
        LOO_JSON (str, optional): The leave one out json file. Defaults to env("LOO_JSON"). See the readme on how to set this file up.
        INSPECT_EVAL_MODEL (str, optional): The model to use for inspecting the evaluation. Defaults to env("INSPECT_EVAL_MODEL").
    Returns:
        asyncio.Future: The future object that will contain the result of the evaluation

    Usage:
        >>> from persona_bench import async_evaluate_model
        >>> from pprint import pprint
        >>> future = async_evaluate_model("gpt-3.5-turbo", evaluation_type="main")
        >>> eval = await future
        >>> pprint(eval[0].results.model_dump())
    """
    # assert that OPENAI_API_KEY, GENERATE_MODE, and INSPECT_EVAL_MODEL are set
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"
    assert GENERATE_MODE is not None, "GENERATE_MODE is not set"
    assert INSPECT_EVAL_MODEL is not None, "INSPECT_EVAL_MODEL is not set"

    eval_fn = None
    if evaluation_type == "main":
        print("Running main evaluation")
        eval_fn = eval_main
    elif evaluation_type == "loo":
        eval_fn = eval_loo
        # assert that LOO_JSON is set
        assert LOO_JSON is not None, "LOO_JSON is not set"
    elif evaluation_type == "intersectionality":
        eval_fn = eval_intersectionality
        # assert that INTERSECTION_JSON is set
        assert INTERSECTION_JSON is not None, "INTERSECTION_JSON is not set"
    elif evaluation_type == "pass_at_k":
        print("Running pass at k")
        eval_fn = eval_pass_at_k
    else:
        raise ValueError(f"Invalid evaluation type: {evaluation_type}")

    return await eval_async(eval_fn, model_str, log_dir=log_dir, seed=seed, limit=N)


def evaluate_model(
    model_str: str,
    evaluation_type: Literal["main", "loo", "intersectionality", "pass_at_k"] = "main",
    log_dir: str = "/tmp/",
    seed: int = None,
    N: int = None,
    OPENAI_API_KEY: str = _env("OPENAI_API_KEY"),
    GENERATE_MODE: Literal[
        "baseline", "output_only", "chain_of_thought", "demographic_summary"
    ] = _env("GENERATE_MODE"),
    INTERSECTION_JSON: str = _env("INTERSECTION_JSON"),
    LOO_JSON: str = _env("LOO_JSON"),
    INSPECT_EVAL_MODEL: str = _env("INSPECT_EVAL_MODEL"),
) -> EvalLog:
    """
    Async. runs persona bench over the model specified by model_str

    Args:
        model_str (str): The model to evaluate
        evaluation_type (Literal["main", "loo", "intersectionality", "pass_at_k"], optional): The evaluation type to run. Defaults to "main".
        log_dir (str, optional): The directory to store the logs. Defaults to "/tmp/".
        seed (int, optional): The seed to use for the evaluation. Defaults to None.
        N (int, optional): The number of samples to use for the evaluation. Defaults to None (all samples).
        OPENAI_API_KEY (str, optional): The openai used for rewriting the model output to be pydantic compliant. Defaults to env("OPENAI_API_KEY").
        GENERATE_MODE (Literal["baseline", "output_only", "chain_of_thought", "demographic_summary"], optional): The mode to use for generating the prompts. Defaults to env("GENERATE_MODE").
        INTERSECTION_JSON (str, optional): The intersectionality json file. Defaults to env("INTERSECTION_JSON"). See the readme on how to set this file up.
        LOO_JSON (str, optional): The leave one out json file. Defaults to env("LOO_JSON"). See the readme on how to set this file up.
        INSPECT_EVAL_MODEL (str, optional): The model to use for inspecting the evaluation. Defaults to env("INSPECT_EVAL_MODEL").

    Returns:
        list[EvalLog]: The result of the evaluation.

    Example:
        >>> from persona_bench import evaluate_model
        >>> from pprint import pprint
        >>> eval = evaluate_model("gpt-3.5-turbo", evaluation_type="main")
        >>> print(eval.results.model_dump())
    """
    return asyncio.run(
        async_evaluate_model(
            model_str,
            evaluation_type,
            log_dir,
            seed,
            N,
            OPENAI_API_KEY,
            GENERATE_MODE,
            INTERSECTION_JSON,
            LOO_JSON,
            INSPECT_EVAL_MODEL,
        )
    )[0]
