# url-anatomy

A tiny Python tool that breaks a URL into its parts and explains what each one means. No dependencies, standard library only.

## Anatomy of a URL

```
  https://user:pass@shop.eu.example.co.uk:8443/products/shoes/index.html?q=red&page=2#reviews
  \___/   \_______/ \_____________________/ \__/\_______________________/ \__________/ \______/
 scheme   userinfo          host            port         path               query     fragment
```

| Part | Meaning |
|------|---------|
| **scheme** | Protocol to use (`http`, `https`, `ftp`...) |
| **userinfo** | Optional `username:password` (discouraged, insecure) |
| **host** | Server address, made of subdomain + domain + suffix |
| **port** | Network port; omitted when it is the scheme's default (443 for https) |
| **path** | Which resource on the server, split by `/` |
| **query** | `key=value` inputs separated by `&` |
| **fragment** | Position inside the page; never sent to the server |

## Usage

```bash
python url_anatomy.py --simple            # simple built-in example
python url_anatomy.py --complex           # complex built-in example
python url_anatomy.py "https://example.com/a?b=c#d"   # your own URL
```

### Simple example

`https://www.example.com/blog/hello-world`

```
scheme           https
host             www.example.com
  suffix         com
  domain         example
  subdomain      www
port             (implied 443)
path             /blog/hello-world
  segment 1      blog
  segment 2      hello-world
```

### Complex example

```
https://user:secret@shop.eu.example.co.uk:8443/products/shoes/running%20shoes/index.html;session=abc?q=red+shoes&page=2&tag=sale&tag=new&lang=en#reviews
```


### Real Example

`www.linkedin.com/in/dguy2003   &   https://github.com/DGUY1-wilm`


![Example output](example.png)



This one shows: embedded credentials, a multi-part suffix (`co.uk`), multiple subdomains, an explicit port, percent-encoding (`%20` = space), a file name, legacy path parameters, repeated query keys, and a fragment. Run `--complex` to see the full explanation.

## Use as a library

```python
from url_anatomy import analyze

for part, value, explanation in analyze("https://example.com/hi?x=1"):
    print(part, value)
```

## Run the tests

```bash
pip install pytest
pytest
```

## Limitations

- Multi-part suffixes (like `co.uk`) are detected from a small built-in list. For full accuracy, use the [Public Suffix List](https://publicsuffix.org).
- IPv6 hosts, internationalized domains, and non-web schemes (`mailto:`) get only basic handling.



MIT
