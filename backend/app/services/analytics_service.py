from app.db.connection import get_connection
from app.algorithms.custom_algorithm import rank_zones_by_revenue


def get_hourly_demand() -> list[dict]:
    sql = """
        SELECT
            pickup_hour,
            COUNT(*) AS trip_count
        FROM trips
        WHERE pickup_hour IS NOT NULL
        GROUP BY pickup_hour
        ORDER BY pickup_hour ASC
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()

    return [dict(r) for r in rows]


def get_revenue_by_zone() -> list[dict]:
    sql = """
        SELECT
            tz.zone_name,
            b.borough_name,
            COUNT(t.trip_id)              AS trip_count,
            ROUND(SUM(t.total_amount), 2) AS total_revenue,
            ROUND(AVG(t.total_amount), 2) AS avg_revenue_per_trip
        FROM trips t
        JOIN taxi_zones tz ON t.pickup_location_id = tz.location_id
        JOIN boroughs   b  ON tz.borough_id        = b.borough_id
        GROUP BY tz.zone_name, b.borough_name
        ORDER BY total_revenue DESC
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()

    result = []
    for r in rows:
        r = dict(r)
        r["total_revenue"]        = float(r["total_revenue"])        if r["total_revenue"]        else 0.0
        r["avg_revenue_per_trip"] = float(r["avg_revenue_per_trip"]) if r["avg_revenue_per_trip"] else 0.0
        result.append(r)
    return result


def get_avg_fare_per_distance() -> list[dict]:
    sql = """
        SELECT
            CASE
                WHEN trip_distance < 1  THEN '0-1 miles'
                WHEN trip_distance < 3  THEN '1-3 miles'
                WHEN trip_distance < 5  THEN '3-5 miles'
                WHEN trip_distance < 10 THEN '5-10 miles'
                WHEN trip_distance < 20 THEN '10-20 miles'
                ELSE                         '20+ miles'
            END                              AS distance_bucket,
            COUNT(*)                         AS trip_count,
            ROUND(AVG(total_amount), 2)      AS avg_fare,
            ROUND(AVG(fare_per_mile), 4)     AS avg_fare_per_mile,
            ROUND(AVG(avg_speed_mph), 2)     AS avg_speed_mph
        FROM trips
        WHERE trip_distance > 0
          AND total_amount  > 0
          AND fare_per_mile IS NOT NULL
        GROUP BY distance_bucket
        ORDER BY MIN(trip_distance) ASC
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()

    result = []
    for r in rows:
        r = dict(r)
        for field in ("avg_fare", "avg_fare_per_mile", "avg_speed_mph"):
            if r.get(field) is not None:
                r[field] = float(r[field])
        result.append(r)
    return result


def get_top_revenue_zones(top_n: int = 10) -> list[dict]:
    sql = """
        SELECT
            tz.zone_name,
            b.borough_name,
            COUNT(t.trip_id)              AS trip_count,
            ROUND(SUM(t.total_amount), 2) AS total_revenue
        FROM trips t
        JOIN taxi_zones tz ON t.pickup_location_id = tz.location_id
        JOIN boroughs   b  ON tz.borough_id        = b.borough_id
        GROUP BY tz.zone_name, b.borough_name
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        raw_rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()

    raw_data = []
    for r in raw_rows:
        r = dict(r)
        r["total_revenue"] = float(r["total_revenue"]) if r["total_revenue"] else 0.0
        raw_data.append(r)

    sorted_data = rank_zones_by_revenue(raw_data)

    return sorted_data[:top_n]