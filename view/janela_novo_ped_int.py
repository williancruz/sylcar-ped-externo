import PySimpleGUI as sg

def JanelaNovoPedInterno():
    sg.theme('SystemDefault')

    layout = [
        [sg.Column(layout=[
            [sg.Text(text='Número', s=15), 
             sg.Input(size=10, k='ipt_num_ped_int')]
        ])],

        [sg.Column(layout=[
            [sg.Text(text='Vendedor', s=15), 
             sg.Input(readonly=True, k='ipt_vendedor', s=25, expand_x=True)]
        ])],

        [sg.Column(layout=[
            [sg.Text(text='Pedido Externo', s=15), 
             sg.Input(size=9, readonly=True, k='ipt_nro_ped_externo'),
             sg.Input(k='id_ped_externo', disabled=True, visible=True, s=9)]
        ])],

        [sg.Column(layout=[
            [sg.Text(text='Situação', s=15), 
             sg.Combo(values=[], readonly=True, s=10,k='cmb_ped_int_status'),
             sg.Checkbox('E', visible=False, k='chb_editando_ped_int')]
        ])],

        [sg.Column(layout=[
            [sg.Button(button_text='Gravar Dados', expand_x=True,
                       k='btn_adicionar_pdint_db')]
        ], expand_x=True)],
    ]

    return sg.Window('Pedido Atrelado', 
                     layout=layout, finalize=True, modal=True,
                     keep_on_top=True) 