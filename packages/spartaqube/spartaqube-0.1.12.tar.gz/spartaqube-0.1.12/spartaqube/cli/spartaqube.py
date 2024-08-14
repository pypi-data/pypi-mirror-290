import typer
import utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app = typer.Typer()


@app.command()
def sparta_bf3c3da6a4(port=None):
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
def sparta_31660d1274():
    """
    Status
    """
    spartaqube_cli.status()


@app.command()
def sparta_d3342d17e6(ip_addr, http_domain):
    """
    Generate api token
    """
    token = spartaqube_cli.token(ip_addr, http_domain)
    print(token)


@app.command()
def sparta_c9cdb5ed34():
    """
    
    """
    print('Hello world!')


if __name__ == '__main__':
    app()

#END OF QUBE
