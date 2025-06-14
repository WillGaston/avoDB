from backend.dbInit import initDBPool
from client.cli.avoDB import avoDB_CLI

if __name__ == '__main__':
    initDBPool()
    avoDB_CLI()