from email.mime import base
import PySimpleGUI as sg
import base64

def codificar_icone():
    # CREDITS: Access Control icon by Icons8
    # https://icons8.com/icon/aSs2sUSslY3b/access-control
    with open ('assets/icons8-access-control-64.png', 'rb') as icone:
        icone_base64 = base64.b64encode(icone.read())

    return icone_base64

def janela_login():
    sg.theme('SystemDefault')

    layout = [
        [sg.Column(
            [
                [sg.Text('USUARIO')],
                [sg.Text('SENHA')],
                [sg.Button('Visitar', expand_x=True, k='btn_auth_visitante')]
            ],
        ),

            sg.Column(
            [
                [sg.Input(size=15, k='ipt_usuario')],
                [sg.Input(password_char='*', size=15, k='ipt_senha')],
                [sg.Button('Autenticar', expand_x=True, k='btn_auth_usuario',
                           bind_return_key=True)]
            ]
        )]
    ]

    return sg.Window('Restrito', layout=layout, finalize=True,
                     element_justification='c',
                     icon=codificar_icone())
