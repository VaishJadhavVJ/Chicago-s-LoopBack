# chicago-loopback

loopback/
  README.md
  .env.example
  requirements.txt
  src/
    loopback/
      __init__.py
      main.py

      core/
        config.py
        errors.py

      db/
        base.py
        session.py
        models.py

      api/
        deps.py
        schemas.py
        routers/
          health.py
          reports.py
          departments.py
          routing.py

      repositories/
        report_repo.py
        issue_repo.py
        queue_repo.py

      services/
        dispatch_service.py
        scoring_service.py
        reporting_service.py
        routing_service.py

      llm/
        client.py
        schemas.py
        prompts/
          issue_triage.md

      integrations/
        maps/
          base.py
          mapbox.py

      utils/
        geo.py