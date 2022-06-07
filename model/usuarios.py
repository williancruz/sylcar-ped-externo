from model.database import Interface as DatabaseInterface
import bcrypt


class Usuario():
    def __init__(self):
        self.dbi = DatabaseInterface()

    def adicionar(self, nome: str, senha: bytes):
        SQL = 'INSERT INTO usuarios (nome, senha) VALUES (?,?)'

        hashed = bcrypt.hashpw(str(senha).encode(), bcrypt.gensalt())

        return self.dbi.executar(sql=SQL, dados=(nome, hashed))

    def autenticar(self, usuario: str, senha: str) -> bool:
        SQL = 'SELECT senha FROM usuarios WHERE nome = ?'

        usuario = self.dbi.recuperar(sql=SQL, 
                                     params=(usuario.lower(),), 
                                     unico=True)

        if usuario:
            hashed = usuario[0]
            if (hashed and bcrypt.checkpw(senha.encode(), hashed)):
                return True
            else:
                return False
        else:
            return False
