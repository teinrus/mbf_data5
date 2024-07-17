import os
import datetime
import asyncio
from dotenv import load_dotenv
from module.DB_send import save_bottle_explosion
from opcua import Client

async def save_file(file_path, data):
    # Функция для сохранения данных в файл
    import json
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def connect_OPC_UA():
    # Загрузка переменных окружения из файла .env
    load_dotenv()
    json_file_path = "tempik.json"  # Убедитесь, что это строка

    data = []
    # Получение значений из переменных окружения
    url = os.getenv("OPC_UA_SERVER_URL")
    node_ids = [os.getenv(f"OPC_UA_NODE_ID_{i}") for i in range(1, 10)]

    # Получение значения переменной OPC_UA_NODE_ID_1
    node_id_1 = os.getenv("OPC_UA_NODE_ID_1")

    trig = False
    # Создание клиента
    client = Client(url)
    try:
        # Подключение к серверу
        client.connect()
        print("Клиент подключен к серверу OPC UA")
        
        # Получение узлов по NodeId с диагностикой
        nodes = []
        for node_id in node_ids:
            try:
                node = client.get_node(node_id)
                nodes.append(node)
            except Exception as e:
                print(f"Произошла ошибка при получении узла с NodeId {node_id}: {e}")
                return

        # # Вывод всех узлов в консоль
        # print("Список всех узлов и их значения:")
        # for node in nodes:
        #     try:
        #         node_id = node.nodeid.to_string()
        #         node_name = node.get_display_name().Text
        #         node_value = node.get_value()
        #         print(f"NodeId: {node_id}, Name: {node_name}, Value: {node_value}")
        #     except Exception as e:
        #         print(f"Произошла ошибка при получении информации об узле: {e}")
        while True:
            # Чтение значений из узлов
            for node_id, node in zip(node_ids, nodes):
                
                try:
                    # node == "ns=6;s=::AsGlobalPV:MES_OUTPUT_DATA.EXPLODED_BOTTLE_FILLING_VALVE":
                    specific_node_id = "ns=6;s=::AsGlobalPV:MES_OUTPUT_DATA.EXPLODED_BOTTLE_FILLING_VALVE"

                    
                    value = node.get_value()
                    if (
                        node_id == "ns=6;s=::AsGlobalPV:MES_OUTPUT_DATA.EXPLODED_BOTTLE_SIGNAL"
                        and value == True 
                        and not trig 
                    ):
                        trig = True
                        node_id_1_value = client.get_node(node_id_1).get_value()
                       
                        save_bottle_explosion(datetime.date.today(), datetime.datetime.now().time(), 1, node_id_1_value)
                        print(node_id_1_value)
                    elif  node_id == "ns=6;s=::AsGlobalPV:MES_OUTPUT_DATA.EXPLODED_BOTTLE_SIGNAL" and value == False:
                        trig = False
                except Exception as e:
                    print(f"Произошла ошибка при чтении значения из узла {node_id}: {e}")


            await asyncio.sleep(5)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Отключение клиента
        client.disconnect()
        print("Клиент отключен от сервера OPC UA")


