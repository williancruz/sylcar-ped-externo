from model.database import Interface as DatabaseInterface

class PedExterno():

    def __init__(self):
        self.dbi = DatabaseInterface()

    def adicionar(self, num, serie, vend, data, obs = None):
        SQL = ('INSERT INTO ped_externos (nro, serie, vend, data, obs) '
               'VALUES (?,?,?,?,?)')

        self.dbi.executar(sql=SQL, dados=(num, serie, vend, data, obs))
        

    def remover(self, cod_ped: str):
        SQL = ('DELETE FROM ped_externos WHERE id = ?')

        self.dbi.executar(sql=SQL, dados=(cod_ped,))

    def atualizar(self, obs: str, ped_id: int):
        SQL = ('UPDATE ped_externos SET obs = ? WHERE id = ?')

        self.dbi.executar(sql=SQL, dados=(obs, ped_id))

    def consultar(self, nro_ped: str, cod_vend: str):
        SQL = ('SELECT id, strftime("%d/%m/%Y", data), printf("%05d",nro), serie, obs '
               'FROM ped_externos '
               'WHERE nro LIKE ? AND vend = ?')

        return self.dbi.recuperar(sql=SQL, params=(f'{nro_ped}%', cod_vend))

    def recuperar_lista(self, cod_vendedor: str):
        SQL = ('SELECT id, strftime("%d/%m/%Y", data), printf("%03d",nro), serie, obs '
               'FROM ped_externos '
               'WHERE vend = ? ORDER BY nro DESC')

        return self.dbi.recuperar(sql=SQL, params=(cod_vendedor,), tam=100)

