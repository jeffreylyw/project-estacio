import psycopg2


class PostgresDB:
    def __init__(self) -> None:
        print("Conexao banco de dados")

    def getConnection(self):
        try:
            self.connection = psycopg2.connect(
                user="adm_mercado",
                password="msi12345",
                port="5432",
                database="msi",
            )
            print("Conexão feita com sucesso")
        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print("Error connection on Database", error)

    def selectAllData(self):
        # Faz conexao ao banco de dados e executa uma query para selecionar todos os clientes da tabela clientes
        try:
            self.getConnection()
            cursor = self.connection.cursor()

            sql_select_query = """SELECT * FROM public.clientes"""

            cursor.execute(sql_select_query)
            clients = cursor.fetchall()

            return [
                {
                    "id": client[0],
                    "nome": client[1],
                    "cpf": client[2],
                    "dt_nascimento": client[3],
                    "email": client[4],
                    "telefone": client[5],
                }
                for client in clients
            ]

        except (Exception, psycopg2.Error) as error:
            print("Error in select operation", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()

    def insertData(self, nome, cpf, dt_nascimento, email, telefone):
        try:
            self.getConnection()
            cursor = self.connection.cursor()

            sql_insert_query = """
                    INSERT INTO public.clientes (nome, cpf, dt_nascimento, email, telefone)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """
            cursor.execute(
                sql_insert_query, (nome, cpf, dt_nascimento, email, telefone)
            )

            # Obter o ID do cliente recém-inserido
            new_client_id = cursor.fetchone()[0]
            self.connection.commit()
            return new_client_id  # Retorna o novo ID

        except (Exception, psycopg2.Error) as error:
            print("Erro ao inserir cliente:", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()

    def updateData(self, client_id, nome, cpf, dt_nascimento, email, telefone):
        try:
            self.getConnection()
            cursor = self.connection.cursor()

            sql_update_query = """
                    UPDATE public.clientes
                    SET nome = %s, cpf = %s, dt_nascimento = %s, email = %s, telefone = %s
                    WHERE id = %s
                """
            cursor.execute(
                sql_update_query, (nome, cpf, dt_nascimento, email, telefone, client_id)
            )
            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar cliente:", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()

    def deleteData(self, client_id):
        try:
            self.getConnection()
            cursor = self.connection.cursor()

            sql_delete_query = """
                    DELETE from public.clientes
                    where id = %s
                """
            cursor.execute(sql_delete_query, (client_id,))

            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Erro ao excluir o cliente", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
