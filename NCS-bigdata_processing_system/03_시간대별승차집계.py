# ==============================================================================
# NCS-bigdata_processing_system/03_시간대별승차집계.py
#
# 실행결과: python 03_시간대별승차집계.py
# [batch] 시간대별 배치 처리 시작
# [batch] 입력 테이블 확인 완료: subway_raw 1,260,000건
# [batch] 시간대별 승차 집계 완료: traffic_hour_summary
# [batch] 시간대별 배치 처리 완료
# ==============================================================================
from database import execute_sql, subway_engine, table_count

def create_hour_summary() -> None:
    execute_sql (
        subway_engine,
        '''
        DROP TABLE IF EXISTS traffic_hour_summary;

        CREATE TABLE traffic_station_summary AS
        SELECT
            "역번호" AS station_no,
            "역명" AS station_name,
            COUNT(*) AS row_count,
            SUM("인원수") AS total_passengers,
            ROUND(AVG("인원수")::numeric, 2) AS avg_passengers
        FROM subway_raw
        GROUP BY "역번호", "역명";
        
        CREATE INDEX idx_traffic_hour_summary_total
        ON traffic_hour_summary(total_passengers DESC);
        '''
    )
    print('[batch] 역별 집계 완료: traffic_hour_summary')
