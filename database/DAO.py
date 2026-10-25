from database.DB_connect import DBConnect
from model.cliente import Cliente

class DAO():

    @staticmethod
    def getGeneri():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct g.GenreId AS id, g.Name AS nome
                from genre g
                order by g.Name
                """

        cursor.execute(query)

        for row in cursor:
            results.append((row["id"],row["nome"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(genere):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT c.CustomerId AS id, c.FirstName AS nome, c.LastName AS cognome,
                       c.Country AS paese, SUM(il.UnitPrice * il.Quantity) AS spesa
                FROM Customer c, InvoiceLine il, Invoice i, Track t
                WHERE il.InvoiceId = i.InvoiceId AND c.CustomerId = i.CustomerId
                  AND t.TrackId = il.TrackId AND t.GenreId = %s
                GROUP BY c.CustomerId, c.FirstName, c.LastName, c.Country
                """
        cursor.execute(query, (genere,))
        for row in cursor:
            c = Cliente(row["id"], row["nome"], row["cognome"], row["paese"], float(row["spesa"]))
            results.append(c)
        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getCoppia(genere):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT i.CustomerId as id, t.AlbumId AS aId
                FROM InvoiceLine il, Invoice i, Track t
                WHERE il.InvoiceId = i.InvoiceId AND t.TrackId = il.TrackId AND t.GenreId = %s
                GROUP BY i.CustomerId, t.AlbumId
                """
        cursor.execute(query, (genere,))
        for row in cursor:
            results.append((row["id"],row["aId"]))
        cursor.close()
        conn.close()
        return results

