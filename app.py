class App():
    def __init__(self):
        App.title('The shape of us!')
        print('\n=> Informe alguns dados para começar:\n')
        App.generate_header()

    @classmethod
    def padding(self):
        print('\n')

    @classmethod
    def generate_header(self):
        print('OBS: O Nível de Atividade varia de 1 (Sedentário) a 4 (Muito Ativo).')
        print(f'Ex: {"1.70":^8s} {"70.0":^22s} {"M":^14s} {"3":^20s} {"20":^10s}\n')

    @classmethod
    def row(self):
        print('*' * 81)

    @classmethod
    def row_table(self):
        print(f'+{"-" * 25}++{"-" * 25}++{"-" * 25}+')

    @classmethod
    def title(self, title: str):
        App.row()
        print(f'*{title:^79s}*')
        App.row()

    @classmethod
    def collect_user_data(self) -> list:
        print(f'{"Altura (m):":^16s}', end='')
        print(f'{"Peso (kg):":^18s}', end='')
        print(f'{"Sexo (M/F):":^18s}', end='')
        print(f'{"Nível de Atividade:":^18s}', end='')
        print(f'{"Idade:":^16s}', end='')

        user_data = input('')
        user_data = user_data.split(' ')
        print()
        App.row()

        return user_data

    @classmethod
    def list_user_data(self, values: list) -> list:
        list = []
        for i in values:
            if i != '':
                if i in 'Mm' or i in 'Ff':
                    list.append(i)
                else:
                    list.append(float(i))
        return list

    @classmethod
    def validate_data(self, values: list) -> list:
        while True:
            try:
                list = App.list_user_data(values)
                user_data = App.generate_dict(list)

            except IndexError:
                print('\nPreencha todos os dados para prosseguir!\n'.upper())
                App.generate_header()
                values = App.collect_user_data()

            except ValueError:
                print('\nValor inválido!\n'.upper())
                App.generate_header()
                values = App.collect_user_data()

            else:
                list = App.list_user_data(values)
                break

        return list

    @classmethod
    def generate_dict(self, list: list) -> dict:
        dic = {
            'altura': float,
            'peso': float,
            'sexo': str,
            'nvl_ativ': float,
            'idade': float
        }

        cont = 0
        for k in dic.keys():
            dic[k] = list[cont]
            cont += 1

        return dic

    @classmethod
    def print_result(self, list: list):
        print()
        App.row()
        print(f'|{str(list[0][0]):^25s}||{str(list[0][1]):^25s}||{str(list[0][2]):^25s}|')
        App.row()

    @classmethod
    # (imc, status)
    def creat_table_imc(self, imc: float, status: str):
        content = [
            ['Tabela de IMC', 'Intervalo', ' Status'],
            ['Menos do que: ', '18,5', 'Abaixo do Peso'],
            ['Entre: ', '18,5 e 24,9', 'Peso Normal'],
            ['Entre: ', '25,0 e 29,9', 'Sobrepeso'],
            ['Entre: ', '30,0 e 34,9', 'Obesidade Grau 1'],
            ['Entre: ', '35,0 e 39,9', 'Obesidade Grau 2'],
            ['Mais do que: ', '40,0', 'Obesidade Grau 3'],
        ]

        # analysingIMC -> status
        result = [['SEU IMC: ', str(imc), status]]
        print()
        for row in range(0, len(content)):
            App.row_table()
            print(f'|{content[row][0]:^25s}||{content[row][1]:^25s}||{content[row][2]:^25s}|')
            if row == 6:
                App.row_table()
                App.print_result(result)

    @classmethod
    def creat_table_qntd_cal(self, dict: dict):
        content = [
            ['Carboidratos: ', dict['carboidratos'], round(float(dict['carboidratos']) / 4.0, 2)],
            ['Proteínas: ', dict['proteinas'], round(float(dict['proteinas']) / 4.0, 2)],
            ['Gorduras: ', dict['gorduras'], round(float(dict['gorduras']) / 9.0, 2)]
        ]

        for row in range(0, len(content)):
            App.row_table()
            print(f'|{str(content[row][0]):^25}||{str(content[row][1]) + " kcal":^25}||{str(content[row][2]) + " g":^25}|')
            App.row_table()
    
    @classmethod
    def imc_option(self, response: dict):
        App.title('Índice de Massa Corporal (IMC)')

        print(f'\n{"O Índice de Massa Corporal (IMC) é um parâmetro":^81s}')
        print(f'{"utilizado para saber se o peso está de acordo com a altura de um":^81s}')
        print(f'{"indivíduo, o que pode interferir diretamente na sua saúde e qualidade de vida.":^81s}')

        App.creat_table_imc(response['imc'], response['status_imc'])

    @classmethod
    def tmb_option(self, response: dict):
        App.title('Taxa Metabólica Basal (TMB)')

        print(f'\n{"A Taxa de Metabolismo Basal (TMB) é a quantidade":^81s}')
        print(f'{"mínima de energia (calorias) necessária para manter as":^81s}')
        print(f'{"funções vitais do organismo em repouso. Essa taxa pode variar":^81s}')
        print(f'{"de acordo com o sexo, peso, altura, idade e nível de atividade física.":^81s}')

        result = [['RESULTADO:', 'SUA TMB:', str(response['tmb']) + ' kcal']]
        App.print_result(result)

    @classmethod
    def qntd_cal_option(self, response: dict):
        nut = response['nutrientes']
        App.title('Quantidade de Calorias')

        print(f'\n{"Calorias são a quantidade de energia que um determinado alimento":^81s}')
        print(f'{"fornece após ser consumido, contribuindo para as funções essenciais do":^81s}')
        print(f'{"organismo, como respiração, produção de hormônios, e funcionamento do cérebro.":^81s}')
        print(f'\n{"Você deve consumir aproximadamente: ":^81s}\n')

        App.creat_table_qntd_cal(nut)
        result = [['RESULTADO:', 'SUA QNTD DE KCAL:', str(response['cal']) + ' kcal']]
        App.print_result(result)

    @classmethod
    def exit_to_app(self):
        print(f'{"Obrigado por usar nosso App!":^79s}')
        App.padding()
        App.row()

    @classmethod
    def menu(self, response: dict):
        while True:
            App.padding()

            print("=> Selecione uma opção:\n")
            print(f'{"1 - IMC":^16s}{"2 - TMB":^18s}{"3 -  QNTD KCAL":^18s}{"4 - SAIR":^18s}{"":2s}', end="\t")
            option = input()

            App.padding()

            if option == '1':
                App.imc_option(response)
            elif option == '2':
                App.tmb_option(response)
            elif option == '3':
                App.qntd_cal_option(response)
            elif option == '4':
                App.exit_to_app()
                break
            else:
                print('Erro: Opção Inválida!')
