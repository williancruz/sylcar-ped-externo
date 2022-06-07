from model.database import Interface as DatabaseInterface

class internos():

    def __init__(self):
        self.dbi = DatabaseInterface()

    def adicionar(self, nro_pedido, faturista, status, id_ped_ext):
        SQL = ('INSERT INTO ped_internos (nro, faturista, status, '
               'fk_num_pedido_externo) VALUES (?,?,?,?)')

        DADOS = (nro_pedido, faturista, status, id_ped_ext)

        self.dbi.executar(sql=SQL, dados=DADOS)

    def remover(self, cod_ped: str):
        SQL = ('DELETE FROM ped_internos WHERE nro = ?')

        self.dbi.executar(sql=SQL, dados=(cod_ped,))

    def atualizar(self, cod_ped: str, status: str):
        SQL = ('UPDATE ped_internos SET status = ? WHERE nro = ?')

        self.dbi.executar(sql=SQL, dados=(status, cod_ped))

    def consultar(self, cod_ped: str):
        pass

    def recuperar_lista(self, id_ped_externo):
        SQL = ('SELECT nro, upper(faturista), status FROM ped_internos '
               'WHERE fk_num_pedido_externo = ? ORDER BY nro ASC')

        return self.dbi.recuperar(sql=SQL, params=(id_ped_externo,))

