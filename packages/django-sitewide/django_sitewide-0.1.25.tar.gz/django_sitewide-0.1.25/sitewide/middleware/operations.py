"""Sitewide Objects/Classes"""

from pathlib import Path
import yaml
from django.conf import settings
from sitewide.middleware.parts import Sitewide


def get_config():
    """get_config() -> dict
    Read configuration from sitewide.yaml at project root dir. If one doesn't
    exist, load defaults"""

    project_yaml = (Path(settings.BASE_DIR) / "sitewide.yaml").resolve()
    yaml_file = (
        project_yaml
        if project_yaml.exists()
        else (Path(__file__).parent / "sitewide.yaml").resolve()
    )
    with open(yaml_file, "rb") as file:
        return yaml.safe_load(file)


class SitewideMiddleware:
    """Django Bridge/connection for Sitewide"""

    def __init__(self, get_response):
        """One-time configuration and initialization."""

        self.get_response = get_response
        self.sitewide = Sitewide(**get_config())

    def __call__(self, request):
        """Middleware caller"""

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_template_response(self, request, response):
        """Update sitewide and Inject back to context_data"""

        changes = response.context_data.get("sitewide", {})
        changes.update({"user": request.user})
        self.sitewide.update(**changes)
        response.context_data["sitewide"] = self.sitewide
        return response
