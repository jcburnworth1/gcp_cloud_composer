CREATE OR REPLACE VIEW {{ params.project_id }}.{{ params.dataset }}.{{ params.view }}
OPTIONS (
    -- Set labels to show source process and step for view
    labels=[
    ('dag-id', '{{ task.dag_id.lower() }}'),
    ('task-id', '{{ task.task_id.lower() }}')
    ]
)
AS (
    SELECT * FROM {{ params.project_id }}.{{ params.dataset }}.{{ params.table }}
    LIMIT 10
)