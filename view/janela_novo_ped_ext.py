import PySimpleGUI as sg

def JanelaNovoPedExterno():
    sg.theme('SystemDefault')

    layout = [
        [sg.Column(layout=[
            [sg.Text(text='Número', s=10), 
             sg.Input(s=8, k='ipt_num_ped_ext')]
        ])],

        [sg.Column(layout=[
            [sg.Text(text='Observação', s=10), 
             sg.Multiline(s=(30,3), k='mln_obs_pedido', justification='l', 
                          no_scrollbar=True)]
        ])],

        [sg.Column(layout=[
            [sg.Text(text='Vendedor', s=10), 
             sg.Input(s=30, disabled=True, k='ipt_vend_ped_externo')]
        ])],

        [sg.Column(layout=[
            [sg.Text(text='Série', s=10), 
             sg.Input(s=2, disabled=True, k='ipt_serie_vend_pedext')]
        ])],

        [sg.Column(layout=[
            [sg.Button(button_text='Gravar Dados', expand_x=True, 
                       k='btn_adicionar_pdext_db')]
        ], expand_x=True)],

        [sg.Column(layout=[
            [sg.Checkbox('E', visible=False, k='chb_editando_ped_ext')]
        ])],

        [sg.Column(layout=[
            [sg.Input(visible=False, k='ipt_id_ped_externo', disabled=True)]
        ])],

    ]

    return sg.Window('Novo Pedido Externo', keep_on_top=True,
                     layout=layout, finalize=True, modal=True) 