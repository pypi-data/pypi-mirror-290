# HathiTrust meta.yml Schma and Validator

A JSON schema and tooling to test whether a meta.yml file in a HathiTrust SIP is valid

## How to Use

If you just want to grab the schema and bring it into an application, you can grab it from `schemas\ht.json`.

If you want to use the built in validator, you can install like so:

```
pipx install htschema
```

and then run the validator against a meta.yml or directory of meta.ymls like so:

```
htschema validate -p the/path/to/your/meta/files
```

## Fixtures 

In case it's useful, a set of meta.ymls are included in the fixtures.