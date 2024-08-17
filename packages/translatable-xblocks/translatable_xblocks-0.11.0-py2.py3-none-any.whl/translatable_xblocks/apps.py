"""
translatable_xblocks Django application initialization.
"""

import pkg_resources
from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginSettings, PluginURLs


class TranslatableXBlocksConfig(AppConfig):
    """
    Configuration for the translatable_xblocks Django application.
    """

    name = "translatable_xblocks"

    plugin_app = {
        PluginURLs.CONFIG: {
            "lms.djangoapp": {
                PluginURLs.NAMESPACE: "translatable_xblocks",
                PluginURLs.APP_NAME: "translatable_xblocks",
                PluginURLs.REGEX: r"^api/translatable_xblocks/",
                PluginURLs.RELATIVE_PATH: "api.urls",
            },
            "cms.djangoapp": {
                PluginURLs.NAMESPACE: "translatable_xblocks",
                PluginURLs.APP_NAME: "translatable_xblocks",
                PluginURLs.REGEX: r"^api/translatable_xblocks/",
                PluginURLs.RELATIVE_PATH: "api.urls",
            },
        },
        PluginSettings.CONFIG: {
            "lms.djangoapp": {
                "production": {
                    PluginSettings.RELATIVE_PATH: "settings.production",
                },
                "common": {
                    PluginSettings.RELATIVE_PATH: "settings.common",
                },
                "devstack": {
                    PluginSettings.RELATIVE_PATH: "settings.devstack",
                },
            },
            "cms.djangoapp": {
                "production": {
                    PluginSettings.RELATIVE_PATH: "settings.production",
                },
                "common": {
                    PluginSettings.RELATIVE_PATH: "settings.common",
                },
                "devstack": {
                    PluginSettings.RELATIVE_PATH: "settings.devstack",
                },
            },
        },
    }

    def ready(self):
        """
        Django startup code: swap edx-platform mapping for blocks with our translated versions.

        See https://discuss.openedx.org/t/override-default-edx-platform-xblock-mappings-without-forking/12441
        """
        # List of translated block types, for dismbiguating entry points
        translated_blocks = ["html", "problem", "video"]

        for block_type in translated_blocks:
            block_entry_points = list(
                pkg_resources.iter_entry_points("xblock.v1", block_type)
            )

            # If we have multiple entry points, ours gets precedence over the Open-edX copy
            if len(block_entry_points) > 1:
                dist = pkg_resources.get_distribution("Open-edX")
                del dist.get_entry_map("xblock.v1")[block_type]
