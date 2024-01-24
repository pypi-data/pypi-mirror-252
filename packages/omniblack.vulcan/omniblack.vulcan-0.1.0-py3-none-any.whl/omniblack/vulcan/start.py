import sys

from operator import attrgetter
from logging import getLogger
from contextlib import suppress
from importlib.resources import path as resource_path
from requests import RequestException
from os import getcwd
from os.path import join

from rich import print

from .dev import DevPackage
from .app import app


from omniblack.repo import find_root, find_packages, YAML

from omniblack.caddy import (
    Caddy,
    FileServerHandler,
    HeadersHandler,
    MatcherList,
    PathMatcher,
    RewriteHandler,
    Route,
    StaticResponseHandler,
    VarsHandler,
    add_standard_headers,
)

PORT = 3000

log = getLogger(__name__)


packages = []


caddy_instance = None


def create_caddy_config(packages):
    root = find_root()

    vars_handler = VarsHandler()
    vars_handler.vars['path_prefix'] = '/docs'
    vars_handler.vars['root'] = join(root, 'docs_build')

    docs_route = Route(
        match=MatcherList(PathMatcher('/docs/*', '/docs')),
        handle=[vars_handler],
        group='static_files',
    )

    pkg_configs = [
        config
        for pkg in packages
        for config in pkg.create_dev_configs()
    ]

    pkg_routes = [
        route
        for config in pkg_configs
        for route in config.routes()
    ] + [docs_route]

    rewriter = Route(
        match=MatcherList(),
        handle=[RewriteHandler(strip_path_prefix='{http.vars.path_prefix}')],
    )

    file_server = Route(
        match=MatcherList(),
        handle=[FileServerHandler(
            pass_thru=True,
            canonical_uris=False,
        )],
    )

    spa_rewrite = Route(
        match=MatcherList(),
        handle=[RewriteHandler(uri='/index.html')],
    )
    headers = HeadersHandler()
    add_standard_headers(headers)
    headers.response.add.add('Cache-Control', 'no-store, max-age=0')

    header_route = Route(
        match=MatcherList(),
        handle=[headers],
    )

    not_found_handler = StaticResponseHandler(
        handler='static_response',
        close=True,
        status_code=404,
        body='Page not found',
    )

    not_found = Route(
        match=MatcherList(),
        handle=[not_found_handler],
    )

    routes = pkg_routes + [
        header_route,
        rewriter,
        file_server,
        spa_rewrite,
        file_server,
        not_found,
    ]

    routes_json = (
        route.model_dump()
        for route in routes
    )

    routes_json = [
        route
        for route in routes_json
        if route is not None
    ]

    return routes_json


@app.command
def print_caddy():
    """
    Print the caddy configuration for this repository.

    Primarily intended for debugging vulcan.
    """

    found_packages = find_packages(Package=DevPackage, sort=True)

    routes = create_caddy_config(found_packages)

    print(routes)


@app.command
def configure_caddy():
    """Configure a caddy server to reverse proxy for dev server."""
    with resource_path(__package__, 'Caddyfile.json') as caddy_file_path:
        SRC_PATH = find_root(getcwd())

        found_packages = find_packages(Package=DevPackage, sort=True)

        routes = create_caddy_config(found_packages)

        caddy = Caddy(
            cwd=SRC_PATH,
            caddy_file=caddy_file_path,
        )

        with caddy, suppress(RequestException):
            caddy.patch('/id/server/routes', json=routes)

            resp = caddy.get('/id/server')
            data = resp.json()

            print('Caddy configured')
            print(data)


@app.command
def k8s_yaml():
    """Print the k8s yamml to for this repository."""
    found_packages = sorted(
        find_packages(Package=DevPackage),
        key=attrgetter('path'),
    )

    with YAML(output=sys.stdout) as yaml:
        yaml.explicit_start = True
        for package in found_packages:
            for config in package.create_dev_configs():
                kube_objects = config.create_kube_objects()
                for kube_object in kube_objects:
                    raw = kube_object.model_dump(exclude_none=True)
                    yaml.dump(raw)


@app.command
def list_images():
    """List all the docker images for this repository."""
    found_packages = find_packages(Package=DevPackage, iter=True)
    image_names = [
        image
        for pkg in found_packages
        for config in pkg.create_dev_configs()
        for image in config.image_names()
    ]

    with YAML(output=sys.stdout) as yaml:
        yaml.dump(image_names)


@app.command
def list_resources():
    """List all tilt resources for this repository."""
    found_packages = find_packages(Package=DevPackage, iter=True)

    resource_names = [
        resource
        for pkg in found_packages
        for config in pkg.create_dev_configs()
        for resource in config.resources()
    ]

    with YAML(output=sys.stdout) as yaml:
        yaml.dump(resource_names)


@app.command
def list():
    """List all packages in this repository."""
    for package in find_packages(Package=DevPackage, iter=True):
        print(package.config)
