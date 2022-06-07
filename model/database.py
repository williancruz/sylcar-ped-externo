import sqlite3


class Interface:

    def __init__(self, db_name='dados.db'):
        self.conn = sqlite3.connect(f'file:{db_name}?mode=rw', uri=True)
        self.cur = self.conn.cursor()

        # Ativa o suporte para chaves estrangeiras
        self.conn.execute('PRAGMA foreign_keys=ON')
        # Move o cache de tabelas para a memória p/ aumentar performance
        self.conn.execute('PRAGMA temp_store = 2')

    def __del__(self):
        self.conn.execute('PRAGMA optimize')
        self.conn.close()

    def executar(self, sql: str, dados: tuple):
        self.cur.execute(sql, dados)
        self.conn.commit()

    def truncar(self):
        """Executa o comando VACUUM no banco de dados.\n
            Docs: https://www.sqlite.org/lang_vacuum.html
        """
        self.conn.execute('PRAGMA locking_mode = EXCLUSIVE')
        self.conn.execute('VACUUM')

    def recuperar(self, **kwargs):
        """Recupera informações do banco de dados.

        Argumentos:
            sql (str): a string SQL a ser executada\n
            unico (bool): Retornar apenas um registro da base. Padrão: False\n
            params (tuple): tupla com argumentos p/ o WHERE (opcional)\n
            tam (int): retorna N registros do banco de dados (opcional)\n

        Retornos:
            tuple: retorna os dados da base (vazia se não tiver mais dados)
        """
        # Recupera os dados do banco de dados
        if ('params' in kwargs):
            self.cur.execute(kwargs['sql'], kwargs['params'])
        else:
            self.cur.execute(kwargs['sql'])

        # Retorna os dados com base no tipo de consulta
        if ('unico' in kwargs and 'tam' not in kwargs):
            return self.cur.fetchone()
        elif ('tam' in kwargs and kwargs['tam'] > 1):
            return self.cur.fetchmany(kwargs['tam'])
        elif ('unico' not in kwargs and 'tam' not in kwargs):
            return self.cur.fetchall()
        else:
            return None
