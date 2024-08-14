import hashlib
import json
import os
import pprint
import time

from passbolt import PassboltAPI

pbcache_path = os.path.expanduser("~/.pbcached")
try:
    caches = json.load(open(pbcache_path))
except json.decoder.JSONDecodeError:
    caches = {}
except FileNotFoundError:
    caches = {}


def get_credentials_multi(key_fd, passphrase, search_names, url=None):
    # Will not cache data. To be used only at application start.

    assert isinstance(search_names, list)

    key = key_fd.read()
    config = {
        "base_url": "https://pass.getnitro.co.in" if url is None else url,
        "private_key": key,
        "passphrase": passphrase,
    }

    p = PassboltAPI(dict_config=config)

    resources = {}
    resource = None
    for item in p.get_resources():
        if item["name"] in search_names:
            resources[item.get("name")] = item

    for name in search_names:
        if name not in resources:
            resources[name] = None
        else:
            resource = resources.get(name)
            res = (
                config.get("gpg_library", "PGPy") == "gnupg"
                and json.loads(p.decrypt(p.get_resource_secret(resource["id"])).data)
                or json.loads(p.decrypt(p.get_resource_secret(resource["id"])))
            )

            username = resource.get("username")
            res["username"] = username
            resources[name] = res

    return resources


def get_credentials(key_fd, passphrase, search_name, url=None):
    assert isinstance(search_name, str)

    cache_key = passphrase + ":" + search_name
    cached = caches.get(cache_key)
    if cached:
        rightnow = int(time.time())
        ex = cached.get("ex")
        if ex > rightnow:
            return cached

    key = key_fd.read()
    config = {
        "base_url": "https://pass.getnitro.co.in" if url is None else url,
        "private_key": key,
        "passphrase": passphrase,
    }

    p = PassboltAPI(dict_config=config)

    resource = next(
        (item for item in p.get_resources() if item["name"] == search_name), None
    )

    if resource is not None:
        res = (
            config.get("gpg_library", "PGPy") == "gnupg"
            and json.loads(p.decrypt(p.get_resource_secret(resource["id"])).data)
            or json.loads(p.decrypt(p.get_resource_secret(resource["id"])))
        )

        username = resource.get("username")
        res["username"] = username
        ex = int(time.time()) + 3600
        res["ex"] = ex
        caches[cache_key] = res
        open(pbcache_path, "w").write(json.dumps(caches))
        return res


if __name__ == "__main__":
    print(
        get_credentials_multi(
            open("../var/passbolt.asc"), "yy", ["Minio", "Sentry", "Tasty"]
        )
    )
