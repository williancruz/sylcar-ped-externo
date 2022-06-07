from model.database import Interface as DatabaseInterface

class Vendedores():

    def __init__(self):
        self.dbi = DatabaseInterface() # Conexão com a base de dados SQLite

    def adicionar(self):
        pass

    def remover(self, cod_vend: str):
        pass

    def atualizar(self, dados: tuple, cod_vend: str):
        pass

    def consultar(self, cod_vend: str):
        SQL = ('SELECT nome, serie_ped '
               'FROM vendedores '
               'WHERE codigo = ?')

        return self.dbi.recuperar(sql=SQL, params=(cod_vend,))

    def recuperar_lista(self):
        SQL = ('SELECT printf("%03d",codigo), nome '
               'FROM vendedores '
               'ORDER BY codigo ASC')

        return self.dbi.recuperar(sql=SQL)

    def recuperar_serie(self, cod_vendedor: str):
        SQL = ('SELECT serie_ped '
               'FROM vendedores '
               'WHERE codigo = ?')

        serie = self.dbi.recuperar(sql=SQL, unico=True, params=(cod_vendedor,))

        return serie[0]