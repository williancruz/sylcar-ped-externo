import PySimpleGUI as sg
import base64


def codificar_icone():
    # CREDITS: Form icon by Icons8
    # https://icons8.com/icon/U1B5BRcYDtbm/form
    with open('assets/icons8-form-64.png', 'rb') as icone:
        icone_base64 = base64.b64encode(icone.read())

    return icone_base64


def overview_pedidos():
    sg.theme('SystemDefault')

    layout_frame_externo = [
        [sg.Text('PESQUISA POR NRO.:'), 
         sg.Input(k='ipt_pesquisa_pedido', expand_x=True, enable_events=True)],
        [sg.Table(headings=('ID', 'DATA', 'PEDIDO', 'SÉRIE', 'OBSERVAÇÃO'),
                  values=[],
                  expand_y=True, expand_x=True,
                  col_widths=(5, 11, 9, 6, 30), auto_size_columns=False,
                  justification='c', select_mode='browse', enable_events=True,
                  k='tbl_ped_externos',
                  visible_column_map=(False, True, True, True, True))],

        [
            sg.Button(button_text='Novo', k='btn_novo_ped_externo'),
            sg.Button(button_text='Editar', k='btn_edita_ped_externo'),
            sg.Button(button_text='Excluir', k='btn_exclui_ped_externo',
                      button_color='red'),
            sg.Text('', text_color='black',expand_x=True, justification='c',
                    k='txt_usuario_ativo')
        ]
    ]

    layout_frame_interno = [
        [sg.Table(headings=('PEDIDO', 'FATURISTA', 'S'),
                  values=[],
                  expand_y=True, expand_x=True,
                  col_widths=(9, 15, 2), auto_size_columns=False,
                  justification='c', select_mode='browse', enable_events=True,
                  k='tbl_ped_internos')],

        [
            sg.Button(button_text='Novo', k='btn_novo_ped_interno'),
            sg.Button(button_text='Editar',
                      k='btn_editar_ped_interno'),
            sg.Button(button_text='Excluir', k='btn_excluir_ped_interno',
                      button_color='red'),
        ]
    ]

    layout_aba_overview = [
        [sg.Frame(title='Selecionar Vendedor',
                  layout=[
                      [sg.Combo(values=[], expand_x=True, enable_events=True,
                                readonly=True, k='cmb_vnd_disponiveis')]
                  ],
                  expand_x=True)
         ],
        [sg.Frame(title='Pedidos Externos (últimos 100)',
                  layout=layout_frame_externo, expand_y=True, expand_x=True),

         sg.Frame(title='Pedidos Atrelados',
                  layout=layout_frame_interno, expand_y=True, expand_x=True)]
    ]

    layout_aba_vendedores = [

    ]

    layout_aba_usuarios = [

    ]

    layout = [
        [sg.Tab('Visão Geral', layout=layout_aba_overview, k='tab_overview')],
        [sg.Tab('Vendedores', layout=layout_aba_vendedores, k='tab_vendedor')],
        [sg.Tab('Usuários', layout=layout_aba_usuarios, k='tab_usuarios')]
    ]

    return sg.Window(title='Organizador de Pedidos Externos :: Ver. 2.2',
                     layout=[
                         [sg.TabGroup(layout=layout, expand_x=True,
                                      expand_y=True)]
                     ],
                     finalize=True, size=(850, 450), icon=codificar_icone())