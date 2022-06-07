from model.usuarios import Usuario
import getpass

usuario = input('Nome do Usuário: ')
senha = getpass.getpass('Senha: ')

usr = Usuario()
print (usr.adicionar(usuario, senha))
