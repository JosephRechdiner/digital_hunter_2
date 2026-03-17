from mysql.connector import MySQLConnection

class MysqlDal:
    """
    Responsible for creating dal operations on MySQL database
    """
    # 1
    @staticmethod
    def get_quality_targets(cnx: MySQLConnection):
        query = """
                SELECT entity_id, target_name, priority_level, movement_distance_km
                FROM targets
                WHERE (priority_level = 1 OR priority_level = 2) AND movement_distance_km > 5;
                """
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    
    # 2
    @staticmethod
    def get_signal_type_count(cnx: MySQLConnection):
        """
        Followed instructions
        """
        query = """
                SELECT signal_type, COUNT(*) AS count
                FROM intel_signals
                GROUP BY signal_type
                ORDER BY count DESC;
                """
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    
    # 3
    @staticmethod
    def get_new_targets(cnx: MySQLConnection):
        """
        Followed instructions
        """
        query = """
                SELECT entity_id, COUNT(*) AS count
                FROM intel_signals
                WHERE priority_level = 99
                GROUP BY entity_id
                ORDER BY count DESC
                LIMIT 3;
                """
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    
    # 4
    @staticmethod
    def get_dangerous_targets(cnx: MySQLConnection):
        """
        Followed instructions
        """
        query = """
            WITH temp1 AS (
                SELECT entity_id, MAX(distance_from_last) AS max_distance
                FROM intel_signals
                WHERE HOUR(timestamp) BETWEEN 8 AND 19
                GROUP BY entity_id
                HAVING max_distance = 0
            ),
            temp2 AS (
                SELECT entity_id, MIN(distance_from_last) AS min_distance
                FROM intel_signals
                WHERE HOUR(timestamp) BETWEEN 0 AND 7 OR HOUR(timestamp) BETWEEN 20 AND 23
                GROUP BY entity_id
                HAVING min_distance >= 10
            )
            SELECT entity_id
            FROM intel_signals
            WHERE entity_id IN (
                SELECT entity_id FROM temp1
                )
                AND entity_id IN (
                SELECT entity_id FROM temp2
                );
                """
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    
    # 5    
    @staticmethod
    def get_target_coords(entity_id: str, cnx: MySQLConnection):
        """
        Followed instructions
        """
        query = """
                SELECT timestamp, reported_lat, reported_lon
                FROM intel_signals
                WHERE entity_id = %s
                ORDER BY timestamp ASC;
                """
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query, (entity_id,))
            result = cursor.fetchall()
        return result
    
    # 6
    # BONUS
    @staticmethod
    def get_runaway_tragets(cnx: MySQLConnection):
        """
        Did not finish
        """
        query = """
                WITH not_destroyed AS (
                    SELECT signal_id, timestamp AS signal_time, entity_id, reported_lat, reported_lon
                    FROM intel_signals
                    WHERE entity_id IN (
                        SELECT DISTINCT damage_assessments.entity_id
                        FROM damage_assessments
                        JOIN attacks
                        ON damage_assessments.entity_id = attacks.entity_id
                        WHERE damage_assessments.result != 'destroyed'
                        )
                    ),
                attackes_merged AS (
                    SELECT not_destroyed.*, attacks.timestamp AS attack_time
                    FROM attacks
                    JOIN not_destroyed
                    ON attacks.entity_id = not_destroyed.entity_id
                    ORDER BY attacks.timestamp
                ),
                less_then_3 AS (
                    SELECT DISTINCT signal_id
                    FROM attackes_merged
                    WHERE (HOUR(attack_time) - HOUR(signal_time)) BETWEEN 0 AND 3
                ),
                more_then_3 AS (
                    SELECT DISTINCT signal_id
                    FROM attackes_merged
                    WHERE HOUR(signal_time) - HOUR(attack_time) BETWEEN 0 AND 3
                ),
                calculated_less_then_3 AS (
                    SELECT *
                    FROM intel_signals
                    WHERE signal_id IN (
                        SELECT * FROM more_then_3
                    )
                )
                select * from calculated_less_then_3;
                """
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
