import typer

from li_aws_helper.aws_config import AWSConfig
from li_aws_helper.sts_client import refresh_token
from li_aws_helper.exceptions import handle_exception

app = typer.Typer()


@app.command()
@handle_exception
def refresh(token: str = typer.Option("", help="Token code")):
    refresh_token(token)
    message = typer.style("Tokens refreshed", fg=typer.colors.GREEN, bold=True)
    typer.echo(message)


@app.command()
@handle_exception
def config():
    region_name = typer.prompt("Region", default='us-east-1', show_default=True)
    access_key = typer.prompt("Access Key")
    secret_key = typer.prompt("Secret Key")
    mfa_arn = typer.prompt("MFA Identifier")

    AWSConfig().configure(region_name, access_key, secret_key, mfa_arn)
    message = typer.style("All Done!", fg=typer.colors.GREEN, bold=True)
    typer.echo(message)


if __name__ == "__main__":
    app()
