import typer
import utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app = typer.Typer()


@app.command()
def sparta_557a9ebc3c(port=None):
    """
    Run spartaqube server
    """
    spartaqube_cli.runserver(port)


@app.command()
def list():
    """
    List nodes
    """
    spartaqube_cli.list()


@app.command()
def sparta_e21bd64391():
    """
    Status
    """
    spartaqube_cli.status()


@app.command()
def sparta_aedb10a7b3(ip_addr, http_domain):
    """
    Generate api token
    """
    token = spartaqube_cli.token(ip_addr, http_domain)
    print(token)


@app.command()
def sparta_6c2910dac8():
    """
    
    """
    print('Hello world!')


if __name__ == '__main__':
    app()

#END OF QUBE
