"""LlamaBot configuration."""
from openai import OpenAI

import typer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .utils import configure_environment_variable


app = typer.Typer()


@app.command()
def api_key(
    provider: str = typer.Argument(default="openai", help="The API provider to use."),
    api_key: str = typer.Option(
        ..., prompt=True, hide_input=True, confirmation_prompt=True
    ),
) -> None:
    """
    Configure the API keys that LlamaBot gets to use.

    .. code-block:: python

        configure(api_key="your_api_key_here")

    .. code-block:: shell

        llamabot configure api-key openai --api-key <your_api_key_here>
        llamabot configure api-key mistral --api-key <your_api_key_here>

    The `provider` argument will be used to set the environment variable.
    The environment variable name is the provider name in all caps,
    followed by `_API_KEY`.
    For example, if you set the provider to `zotero`,
    then the environment variable will be `ZOTERO_API_KEY`.
    Alternatively, if you set the provider to `mistral`,
    then the environment variable will be `MISTRAL_API_KEY`.

    :param api_key: The API key to be used for authentication.
    """
    configure_environment_variable(
        env_var=f"{provider.upper()}_API_KEY", env_value=api_key
    )


@app.command()
def default_model(model_name=None):
    """Configure the default model for llamabot.

    If no model name is provided,
    or if the model name is not one of those that the user's API key has access to,
    then the user will be prompted for a model name.

    :param model_name: The name of the model to be used for default
    """
    from dotenv import load_dotenv

    from llamabot.config import llamabotrc_path

    load_dotenv(llamabotrc_path)

    client = OpenAI()

    model_list = client.models.list()
    available_models = [x.id for x in model_list if "gpt" in x.id]
    available_models.sort()

    if model_name in available_models:
        configure_environment_variable(
            env_var="DEFAULT_LANGUAGE_MODEL", env_value=model_name
        )
        return

    completer = WordCompleter(available_models)

    typer.echo("These are the GPT models available to you:")
    for model in available_models:
        typer.echo(model)

    while True:
        default_model = prompt(
            "Please type the name of the model you'd like to use: ",
            completer=completer,
            complete_while_typing=True,
            default=available_models[-1],
        )
        if default_model in available_models:
            configure_environment_variable(
                env_var="DEFAULT_LANGUAGE_MODEL", env_value=default_model
            )
            break
