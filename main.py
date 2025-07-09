from backend.dbInit import closeDBPool, initDBPool
from client.cli.avoDB import avoDB_CLI

def main():
    initDBPool()
    avoDB_CLI()
    closeDBPool()

if __name__ == '__main__':
    main()