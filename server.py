# imports the necessary libraries to run the server,
# store and process the data passed by 'client.py'
import socket, json

# create a socket object
print('ECHO SERVER para cálculo do IMC')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the IP address of the local machine (localhost)
# and use any port to host the server
host = '127.0.0.1'
port = 9999

# binds the server to the previously specified port
server_socket.bind((host, port))

# start listening requests
server_socket.listen()
print(f'Serviço rodando na porta {port}.')

while True:
    # establish a connection
    client_socket, addr = server_socket.accept()
    print(f'Conectado a {str(addr)}')

    # receive client data
    received = client_socket.recv(1024).decode()
    print(f'Os dados recebidos do cliente são: {received}')

    # server processing incoming data
    received = json.loads(received)

    # generate IMC
    def generate_imc(dict: dict) -> float:
        """Generates the client's Body Mass Index (BMI or IMC) value.

        Based on the 'dict' parameter, the function collects the values of the 'altura' and 'peso' keys
        (both provided by the client) and uses them to calculate the client's IMC value.

        Args:
            dict: A dictionary containing client-supplied values.
            Among them is the values of the 'altura' and 'peso' keys used in this function.

        Returns:
            A float that indicates the value of the client's Body Mass Index (BMI or IMC),
            using the values of the 'altura' and 'peso' keys (both belonging to the 'dict' parameter),
            rounded to two decimal points. For example:

            round(float(70 / (1.70 ** 2)), 2) = 24.22
        """

        height = dict['altura']
        weight = dict['peso']
        return round(float(weight / (height ** 2)), 2)

    # adding the IMC to data sent by the user
    received['imc'] = generate_imc(received)

    # analyse IMC and generate status
    def analyse_imc(imc: float) -> str:
        """Analyzes the value of the Body Mass Index (BMI or IMC) of the client.

        Based on the 'imc' parameter, the function collects its value (calculated through another function)
        and uses it to assign a value to the 'status' variable.

        Args:
            imc: A float containing the client's IMC value.

        Returns:
            A string that indicates the current status of the client,
            based on the client's IMC value. For example:

            imc = 24.22\n
            status = 'Peso Normal'
        """

        if imc > 0 and imc < 18.5:
            status = 'Abaixo do Peso'
        elif imc <= 24.9:
            status = 'Peso Normal'
        elif imc <= 29.9:
            status = 'Sobrepeso'
        elif imc <= 34.9:
            status = 'Obesidade Grau 1'
        elif imc <= 39.9:
            status = 'Obesidade Grau 2'
        elif imc <= 40.0:
            status = 'Obesidade Grau 1'
        else:
            status = 'Valores inválidos!'

        return status

    # adding the status of the IMC to data sent by the user
    received['status_imc'] = analyse_imc(received['imc'])

    # generate TMB
    def generate_tmb(dict: dict) -> float:
        """Generates the value of the client's Basal Metabolic Rate (BMR or TMB).

        Based on the 'dict' parameter, the function collects the values of the keys 'sexo', 'peso', 'altura' and 'idade'
        (all provided by the client), and uses them to calculate the value of 'tmb'.

        Args:
            dict: A dictionary containing client-supplied values.
            Among them is the values of the 'sexo', 'peso', 'altura' and 'idade' keys used in this function.

        Returns:
            A float that indicates the value of the Basal Metabolic Rate (BMR or TMB) of the client,
            using the value of the key 'sexo' to verify the gender of the client and the values
            of the keys 'peso', 'altura' and 'idade' (all belonging to the parameter 'dict'). For example:

            sex = 'M'\n
            tmb = 5 + (10 * 70) + (6.25 * (1.70 * 100)) - (5 * 20) = 1667.5
        """

        sex = dict['sexo']

        if sex in 'Mm':
            tmb = 5 + (10 * dict['peso']) + (6.25 * (dict['altura'] * 100)) - (5 * dict['idade'])
        else:
            tmb = (10 * dict['peso']) + (6.25 * (dict['altura'] * 100)) - (5 * dict['idade']) - 5

        return tmb

    # adding the TMB to data sent by the user
    received['tmb'] = generate_tmb(received)

    # generate kcal
    def generate_cal(dict: dict) -> float:
        """Generates the amount of calories that the client has.

        Based on the 'dict' parameter, the function collects the value of the key 'nvl_ativ'
        (supplied by the client) and 'tmb' (calculated through another function) and uses them
        to calculate the value of 'fator_ativ' and the amount of kcal of the client.

        Args:
            dict: A dictionary containing client-supplied values.
            Among them is the values of the 'nvl_ativ' and 'tmb' keys used in this function.

        Returns:
            A float that indicates the client's kcal amount, using the value of the 'tmb' key of the 'dict' parameter
            and the 'fator_ativ' variable, rounded to two decimal points. For example:

            round((1667.5 * 1.725), 2) = 2876.44
        """

        if dict['nvl_ativ'] == 1:
            fator_ativ = 1.2
        elif dict['nvl_ativ'] == 2:
            fator_ativ = 1.375
        elif dict['nvl_ativ'] == 3:
            fator_ativ = 1.725
        else:
            fator_ativ = 1.9

        return round((dict['tmb'] * fator_ativ), 2)

    # adding the kcal to data sent by the user
    received['cal'] = generate_cal(received)

    # generate nutrients
    def generate_nutrients(dict: dict) -> dict:
        """Generates the amount of nutrients needed for personal consumption.

        Based on the 'dict' parameter, the function collects the value of the 'cal' key
        (calculated through another function) and uses it to calculate the values of 'carb', 'prot' and 'fat'.

        Args:
            dict: A dictionary containing client-supplied values.
            Among them is the value of the 'cal' key used in this function.

        Returns:
            A dict containing three float values that will be laid out in a table. For example:

            {'carboidratos': 1294.4,
            'proteinas': 862.93,
            'gorduras': 719.11}
        """

        carb = str(round((dict['cal'] * 0.45), 2))
        prot = str(round((dict['cal'] * 0.3), 2))
        fat = str(round((dict['cal'] * 0.25), 2))

        return {'carboidratos': carb, 'proteinas': prot, 'gorduras': fat}

    # adding the nutrients to data sent by the user
    received['nutrientes'] = generate_nutrients(received)
    print(f'O resultado do processamento é {received}')

    # serialising data
    result = json.dumps(received)

    # send a result (in bytes)
    client_socket.send(result.encode('ascii'))
    print('Os dados do cliente foram enviados com sucesso!')

    # finish a connection
    client_socket.close()
