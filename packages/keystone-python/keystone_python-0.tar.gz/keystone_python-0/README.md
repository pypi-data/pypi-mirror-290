# Keystone Packages

## Contributing

### Add new project

```shell
hatch new <project_name>
```

The `<project_name>` follows the following convention:

* If the pip package will be internal (lives in gitlab), then name the project `keystone-<name>`
* If the pip package will live in pjdev account on pypi.org, then name the project `pjdev-<name>`

## Publish to Pypi

```powershell
./publish_to_project_repo.ps1 -projectId pypi -deployTokenUser __token__
```

> for the `deployToken` see `Keeper`
