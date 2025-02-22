"""migration for triggers :/

Revision ID: beee9ddc708e
Revises: e9d7493c8df9
Create Date: 2025-02-22 22:43:47.160675

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "beee9ddc708e"
down_revision: Union[str, None] = "e9d7493c8df9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    CREATE OR REPLACE FUNCTION update_event_averages()
        RETURNS TRIGGER AS $$
    BEGIN
        -- Insert or update daily event stats
        INSERT INTO event_stats_daily (eid, date, avg_response_time, uptime, count, updated_at)
        VALUES (
                   NEW.eid,
                   DATE_TRUNC('day', NEW.created_at),
                   ROUND(NEW.time_took::numeric, 2)::double precision,  -- Explicit cast to numeric before rounding
                   CASE
                       WHEN NEW.status_code >= 500 THEN 0
                       ELSE 100
                       END,
                   1,
                   NOW()
               )
        ON CONFLICT (eid, date)
            DO UPDATE SET
                          avg_response_time = ROUND(
                                  ((event_stats_daily.avg_response_time * event_stats_daily.count + NEW.time_took)
                                      / (event_stats_daily.count + 1))::numeric, 2
                                              )::double precision,
                          count = event_stats_daily.count + 1,
                          uptime = ROUND(
                                  ((event_stats_daily.uptime * event_stats_daily.count +
                                    CASE
                                        WHEN NEW.status_code >= 500 THEN 0
                                        ELSE 100
                                        END)
                                      / (event_stats_daily.count + 1))::numeric, 2
                                   )::double precision,
                          updated_at = NOW();
    
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    )

    op.execute(
        """
    -- Create trigger on event_logs after insert
    CREATE or replace TRIGGER  trigger_update_event_averages
        AFTER INSERT ON event_logs
        FOR EACH ROW
    EXECUTE FUNCTION update_event_averages();
    """
    )


def downgrade() -> None:
    op.execute("""DROP TRIGGER IF EXISTS trigger_update_event_averages""")
    op.execute("""DROP FUNCTION IF EXISTS update_event_averages""")
