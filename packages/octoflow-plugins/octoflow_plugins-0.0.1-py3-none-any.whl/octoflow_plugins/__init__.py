from octoflow.core.plugins import Package

__all__ = [
    "package",
]

__version__ = "0.0.1"

package = Package(
    "plugins",
    modules=[
        {
            "name": ".tracking",
            "package": "octoflow_plugins",
        },
    ],
)
