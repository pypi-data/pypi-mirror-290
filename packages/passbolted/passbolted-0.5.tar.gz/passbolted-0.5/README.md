# Password Extractor by name using py-passbolt.



# Build and Upload

```
make build
make upload
```

# Usage

```
passbolted.get_credentials_multi(file_like_passbolted_asc_object, passphrase, [list, of, keys])
```

or

```
passbolted.get_credentials(file_like_passbolted_asc_object, passphrase, key)
```

This method will also cache the keys.


