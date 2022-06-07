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

    def recuperar(self, sql: str, params: tuple = (), tam: int = 0,
                  unico: bool = False) -> tuple | None:
        """Recupera informações do banco de dados.

        Argumentos:
            sql (str): a string DQL a ser executada\n
            unico (bool): Retornar apenas um registro da base. Padrão: False\n
            params (tuple): tupla com argumentos p/ o WHERE (opcional)\n
            tam (int): retorna N registros do banco de dados (opcional)\n

        Retornos:
            tuple: retorna os dados da base (vazia se não tiver mais dados)
            none: em caso de configuração incorreta dos parâmetros
        """
        # RECUPERAR OS DADOS DA BASE DE DADOS
        if len(params) > 0:
            self.cur.execute(sql, params)
        else:
            self.cur.execute(sql)

        # RETORNOS DE CONSULTA
        if unico:  # único registro, ignora os outros parâmetros
            return self.cur.fetchone()
        elif (not unico and tam > 1):  # retorna N elementos da base
            return self.cur.fetchmany(tam)
        elif not unico:  # retorna tudo e ignora os outros parâmetros
            return self.cur.fetchall()
        else:
            return None
