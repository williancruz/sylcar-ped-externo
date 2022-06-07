from datetime import datetime
import sqlite3
import pyperclip
import PySimpleGUI as sg
from model.usuarios import Usuario
from model.vendedor import Vendedores
from model.externos import PedExterno
from model.internos import internos
from view.janela_novo_ped_ext import JanelaNovoPedExterno
from view.janela_novo_ped_int import JanelaNovoPedInterno
from view.janela_login import janela_login
from view.janela_principal import overview_pedidos


usuario_ativo = str()

login, pedidos, ped_ext, ped_int = janela_login(), None, None, None


def popular_tabela_externos(cod_vendedor: int):
    ped_externo = PedExterno()
    lista_pedidos = ped_externo.recuperar_lista(cod_vendedor)

    pedidos['tbl_ped_externos'].update(values=[])
    pedidos['tbl_ped_internos'].update(values=[])
    pedidos['tbl_ped_externos'].update(values=lista_pedidos)


def popular_tabela_internos(id_ped_externo: int):
    ped_interno = internos()
    lista_pedidos = ped_interno.recuperar_lista(id_ped_externo)

    pedidos['tbl_ped_internos'].update(values=[])
    pedidos['tbl_ped_internos'].update(values=lista_pedidos)


def popular_combo_vendedores():
    lista_vendedores = []

    vendedor = Vendedores()
    dados_db = vendedor.recuperar_lista()

    for i in dados_db:
        cod, nome = i
        lista_vendedores.append(f'{cod} - {nome}')

    pedidos['cmb_vnd_disponiveis'].update(values=lista_vendedores)


def pegar_ped_externo_tabela():
    if (values['tbl_ped_externos']):
        dados_tabela = pedidos['tbl_ped_externos'].get()
        linha = values['tbl_ped_externos'][0]

        # 0 - ID do registro
        # 1 - Data do Pedido
        # 2 - Nro. do Pedido
        # 3 - Série do Pedido
        # 4 - Observação
        return dados_tabela[linha]


def pegar_ped_interno_tabela():
    if (values['tbl_ped_internos']):
        dados_tabela = pedidos['tbl_ped_internos'].get()
        linha = values['tbl_ped_internos'][0]

        # 0 - Nro. do Pedido
        # 1 - Faturista
        # 2 - Status
        return dados_tabela[linha]


while True:
    window, event, values = sg.read_all_windows()

    '''
        CONTROLES DE FECHAMENTO E ABERTURA DE JANELAS :::::::::::::::::::::::::
    '''

    if (window == login and event == sg.WINDOW_CLOSED):
        break

    if (window == ped_ext and event == sg.WIN_CLOSED):
        ped_ext.close()

    if (window == ped_int and event == sg.WIN_CLOSED):
        ped_int.close()

    if (window == pedidos and event == sg.WIN_CLOSED):
        usuario_ativo = ''
        pedidos.close()
        login.un_hide()
        login['ipt_usuario'].update(value='')
        login['ipt_senha'].update(value='')

    '''
        CONTROLES DE AUTENTICAÇÃO :::::::::::::::::::::::::::::::::::::::::::::
    '''
    # USUÁRIO CLICA NO BOTÃO 'VISITANTE' NA TELA DE LOGIN
    if (window == login and event == 'btn_auth_visitante'):
        login.hide()
        pedidos = overview_pedidos()

        pedidos["btn_novo_ped_externo"].update(disabled=True)
        pedidos["btn_edita_ped_externo"].update(disabled=True)
        pedidos["btn_exclui_ped_externo"].update(disabled=True)
        pedidos["btn_novo_ped_interno"].update(disabled=True)
        pedidos["btn_editar_ped_interno"].update(disabled=True)
        pedidos["btn_excluir_ped_interno"].update(disabled=True)
        pedidos["txt_usuario_ativo"].update(value=':: VISITANTE ::',
                                            background_color='red',
                                            text_color='white')
        pedidos["tab_vendedor"].update(visible=False)
        pedidos["tab_usuarios"].update(visible=False)

        popular_combo_vendedores()

    # USUÁRIO FAZ AUTENTICAÇÃO USANDO LOGIN E SENHA
    if (window == login and event == 'btn_auth_usuario'):
        nome = str(values['ipt_usuario'])
        senha = str(values['ipt_senha'])

        if (nome.isalnum() and senha.isalnum()):
            usuario = Usuario()

            try:
                if (usuario.autenticar(nome, senha)):
                    login.hide()
                    usuario_ativo = nome.capitalize()
                    pedidos = overview_pedidos()  # Janela Pedidos
                    pedidos["txt_usuario_ativo"].update(
                        value=f'USUÁRIO: {usuario_ativo.upper()}')
                    popular_combo_vendedores()
                else:
                    login['ipt_senha'].update(value='')
                    sg.PopupOK('Usuário ou Senha inválido', title='Oops...')
            except Exception as err:
                sg.PopupOK(f'{err}', title='Oops...')
        else:
            sg.PopupOK('Usuário e/ou Senha em branco!', title='Oops...')

    '''
        AÇÕES RELACIONADAS COM AS TABELAS NA JANELA PRINCIPAL :::::::::::::::::
    '''
    # CARREGA OS PEDIDOS EXTERNOS DO VENDEDOR SELECIONADO
    if (window == pedidos and event == 'cmb_vnd_disponiveis'):
        if values['cmb_vnd_disponiveis']:
            pedidos['ipt_pesquisa_pedido'].update(value='')
            cod_vendedor = values['cmb_vnd_disponiveis'][0:3]
            popular_tabela_externos(cod_vendedor)

    # CARREGA A LISTA DE PEDIDOS INTERNOS AO CLICAR NA TABELA DOS EXTERNOS
    if (window == pedidos and event == 'tbl_ped_externos'):
        selecao_tabela = pegar_ped_externo_tabela()
        if (selecao_tabela is not None):
            id_pedido_externo = selecao_tabela[0]
            popular_tabela_internos(id_pedido_externo)

    # USUÁRIO CLICA EM UMA LINHA DA TABELA 'PEDIDOS INTERNOS'
    if (window == pedidos and event == 'tbl_ped_internos'):
        selecao_tabela = pegar_ped_interno_tabela()
        if (selecao_tabela is not None):
            nro_pedido_interno = selecao_tabela[0]
            pyperclip.copy(nro_pedido_interno)

    # PESQUISAR PEDIDO EXTERNO
    if (window == pedidos and event == 'ipt_pesquisa_pedido'):
        cod_vendedor = str(values['cmb_vnd_disponiveis'][0:3])
        nro_pedido = str(values['ipt_pesquisa_pedido'])

        if (cod_vendedor and nro_pedido):
            ped_externo = PedExterno()
            dados_pedido = ped_externo.consultar(nro_pedido, cod_vendedor)
            pedidos['tbl_ped_externos'].update(values=[])
            pedidos['tbl_ped_internos'].update(values=[])
            pedidos['tbl_ped_externos'].update(values=dados_pedido)
        elif (cod_vendedor and not nro_pedido):
            popular_tabela_externos(cod_vendedor)
        else:
            pass

    '''
        AÇÕES RELACIONADAS A ABA PEDIDOS ::::::::::::::::::::::::::::::::::::::
    '''
    # BOTÃO NOVO PEDIDO EXTERNO
    if (window == pedidos and event == 'btn_novo_ped_externo'):
        if (values['cmb_vnd_disponiveis']):
            ped_ext = JanelaNovoPedExterno()
            vendedor = Vendedores()

            vend_selecionado = values['cmb_vnd_disponiveis']
            serie_vendedor = vendedor.recuperar_serie(vend_selecionado[:3])

            ped_ext['ipt_vend_ped_externo'].update(value=vend_selecionado)
            ped_ext['ipt_serie_vend_pedext'].update(value=serie_vendedor)
            ped_ext['chb_editando_ped_ext'].update(value=False)
        else:
            sg.PopupQuickMessage('Primeiro selecione um vendedor da lista')

    # BOTÃO EDITAR PEDIDO EXTERNO
    if (window == pedidos and event == 'btn_edita_ped_externo'):
        if (values['tbl_ped_externos']):
            ped_ext = JanelaNovoPedExterno()
            vendedor = Vendedores()

            vend_selecionado = values['cmb_vnd_disponiveis']
            serie_vendedor = vendedor.recuperar_serie(vend_selecionado[:3])
            ped_selecionado = pegar_ped_externo_tabela()

            ped_ext['ipt_num_ped_ext'].update(value=ped_selecionado[2],
                                              disabled=True)
            ped_ext['ipt_vend_ped_externo'].update(value=vend_selecionado)
            ped_ext['ipt_serie_vend_pedext'].update(value=serie_vendedor)
            ped_ext['chb_editando_ped_ext'].update(value=True)
            ped_ext['ipt_id_ped_externo'].update(value=ped_selecionado[0])
            ped_ext['mln_obs_pedido'].update(value=ped_selecionado[4])

    # BOTÃO EXCLUIR PEDIDO EXTERNO
    if (window == pedidos and event == 'btn_exclui_ped_externo'):
        if (values['tbl_ped_externos']):
            layout_conf_exclusao = [
                [sg.T(text=('Deseja mesmo excluir este item?\n'
                            'Esta operação é irreversível!!!'))],
                [sg.Yes('Sim', s=5, k='_excluir_sim_', button_color='Red'),
                 sg.No('Não', s=5, k='_excluir_nao_')]]

            r, _ = sg.Window('Confirmar exclusão', layout_conf_exclusao,
                             disable_close=True).read(close=True)

            if r == '_excluir_sim_':
                try:
                    ped_selecionado = pegar_ped_externo_tabela()[0]  # ID no DB

                    if (ped_selecionado):
                        pd_externo = PedExterno()
                        pd_externo.remover(ped_selecionado)

                        sg.PopupQuickMessage('Registro Removido')

                        cod_vendedor = values['cmb_vnd_disponiveis'][0:3]
                        popular_tabela_externos(cod_vendedor)
                except Exception as err:
                    print(err)

    # GRAVAR PEDIDO EXTERNO DO BANCO DE DADOS
    if (window == ped_ext and event == 'btn_adicionar_pdext_db'):
        pedido_externo = PedExterno()
        vendedor = Vendedores()

        nro_pedido = values['ipt_num_ped_ext']
        id_pedido_externo = values['ipt_id_ped_externo']
        observacao = values['mln_obs_pedido']
        data = datetime.today().isoformat()

        cod_vendedor = values['ipt_vend_ped_externo'][0:3]
        serie_vendedor = vendedor.recuperar_serie(cod_vendedor)

        if (nro_pedido and str(nro_pedido).isnumeric()):
            if (values['chb_editando_ped_ext']):
                pedido_externo.atualizar(values['mln_obs_pedido'],
                                         int(id_pedido_externo))

                ped_ext.close()
                sg.PopupQuickMessage('Registro Atualizado')
                pedidos['ipt_pesquisa_pedido'].update(value='')
            else:
                pedido_externo.adicionar(int(nro_pedido), serie_vendedor,
                                         int(cod_vendedor), data, observacao)
                ped_ext.close()
                popular_tabela_externos(cod_vendedor)
                sg.PopupQuickMessage('Registro Inserido')
                pedidos['ipt_pesquisa_pedido'].update(value='')
        else:
            sg.PopupQuickMessage('Nro. do PED em branco ou contém letras...')

        popular_tabela_externos(cod_vendedor)

    # BOTÃO NOVO PEDIDO INTERNO
    if (window == pedidos and event == 'btn_novo_ped_interno'):
        if (values['tbl_ped_externos']):
            ped_int = JanelaNovoPedInterno()
            vendedor = Vendedores()

            vend_selecionado = values['cmb_vnd_disponiveis']
            serie_vendedor = vendedor.recuperar_serie(vend_selecionado[:3])
            ped_selecionado = pegar_ped_externo_tabela()  # Nro. PED

            ped_int['ipt_vendedor'].update(value=vend_selecionado[6:])
            ped_int['ipt_nro_ped_externo'].update(value=ped_selecionado[2])
            ped_int['cmb_ped_int_status'].update(values=('Aberto', 'Faturado'),
                                                 value='Aberto')
            ped_int['id_ped_externo'].update(value=ped_selecionado[0])
            ped_int['chb_editando_ped_int'].update(value=False)
        else:
            sg.PopupQuickMessage('Selecione um PED externo primeiro')

    # BOTÃO EXCLUIR PEDIDO INTERNO
    if (window == pedidos and event == 'btn_excluir_ped_interno'):
        if (values['tbl_ped_internos']):
            layout_conf_exclusao = [
                [sg.T(text=('Deseja mesmo excluir este item?\n'
                            'Esta operação é irreversível!!!'))],
                [sg.Yes('Sim', s=5, k='_excluir_sim_', button_color='Red'),
                 sg.No('Não', s=5, k='_excluir_nao_')]]

            r, _ = sg.Window('Confirmar exclusão', layout_conf_exclusao,
                             disable_close=True).read(close=True)

            if r == '_excluir_sim_':
                try:
                    int_selecionado = pegar_ped_interno_tabela()
                    ext_selecionado = pegar_ped_externo_tabela()

                    pedido = internos()
                    pedido.remover(int_selecionado[0])

                    sg.PopupQuickMessage('Registro Excluído')

                    popular_tabela_internos(ext_selecionado[0])
                except Exception as err:
                    print(err)
            else:
                sg.PopupQuickMessage('Exclusão cancelada')
        else:
            sg.PopupQuickMessage('Primeiramente selecione um pedido...')

    # BOTÃO EDITAR PEDIDO INTERNO
    if (window == pedidos and event == 'btn_editar_ped_interno'):
        if (values['tbl_ped_internos']):
            ped_selecionado = pegar_ped_interno_tabela()

            if (ped_selecionado[2] == 'C'):
                msg = 'Edição não permitida: o pedido está cancelado.'
                sg.PopupQuickMessage(msg)
            else:
                ped_int = JanelaNovoPedInterno()
                pedido_ext = pegar_ped_externo_tabela()
                vend_selecionado = values['cmb_vnd_disponiveis']

                ped_int['ipt_num_ped_int'].update(value=ped_selecionado[0],
                                                  disabled=True)
                ped_int['ipt_vendedor'].update(value=vend_selecionado[6:])
                ped_int['ipt_nro_ped_externo'].update(value=pedido_ext[2])
                ped_int['id_ped_externo'].update(value='')
                ped_int['cmb_ped_int_status'].update(values=('Faturado',
                                                             'Cancelado'),
                                                     value='Faturado')
                ped_int['chb_editando_ped_int'].update(value=True)
                ped_int['id_ped_externo'].update(value=pedido_ext[0])
        else:
            sg.PopupQuickMessage('Primeiramente selecione um pedido...')

    # GRAVAR PEDIDO INTERNO DO BANCO DE DADOS
    if (window == ped_int and event == 'btn_adicionar_pdint_db'):
        nro_pedido = values['ipt_num_ped_int']
        id_pedext = values['id_ped_externo']
        status = values['cmb_ped_int_status'][:1]
        cod_vendedor = values['ipt_vendedor'][0:3]
        pedido = internos()

        if (str(nro_pedido).isnumeric() and len(nro_pedido) == 8):
            try:
                if values['chb_editando_ped_int']:
                    pedido.atualizar(nro_pedido, status)
                    sg.PopupQuickMessage('Registro Atualizado')
                    pedidos['ipt_pesquisa_pedido'].update(value='')
                else:
                    pedido.adicionar(nro_pedido, usuario_ativo, status,
                                     id_pedext)
                    sg.PopupQuickMessage('Registro Inserido')
                    pedidos['ipt_pesquisa_pedido'].update(value='')
                ped_int.close()
                popular_tabela_internos(id_pedext)
            except sqlite3.IntegrityError as err:
                if 'UNIQUE constraint failed: ped_internos.nro' in str(err):
                    sg.popup_ok((':: Erro de Integridade ::\n\n'
                                 'PED interno já cadastrado!'),
                                title='Oops!', keep_on_top=True,
                                modal=True)
        else:
            sg.PopupQuickMessage(
                'Nro. do PED contém letras ou está incompleto')
