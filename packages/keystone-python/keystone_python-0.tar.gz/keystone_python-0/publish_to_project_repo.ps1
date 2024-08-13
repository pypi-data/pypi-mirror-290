#!/usr/local/bin/pwsh

param(
    [Parameter(mandatory = $true)]
    [String] $projectId,
    [Parameter(mandatory = $true)]
    [String] $deployToken,
    [Parameter(mandatory = $true)]
    [String] $deployTokenUser,
    [Parameter(mandatory = $true)]
    [String] $projectFolder,
    [String] $version = ""
)

$cwd = $( Get-Location )
$root = "$PSScriptRoot"

try
{
    Set-Location "$root"

    if ($version -eq "")
    {
        $version = "$( git describe --tag )"
    }

    Write-Output "$version"
    docker build -t keystone_python $root

    if ($projectId -eq "pypi")
    {
        $publishUrl = "https://upload.pypi.org/legacy/"
    }
    else
    {
        $publishUrl = "https://gitlab.purplejay.net/api/v4/projects/$projectId/packages/pypi"
    }

    docker run `
        --rm `
        -it `
        -e "HATCH_INDEX_AUTH=$deployToken" `
        -e "HATCH_INDEX_USER=$deployTokenUser" `
        -e "PROJECT_PATH=/app/$projectFolder" `
        -e "PUBLISH_URL=$publishUrl" `
        -e "version=$version" `
        keystone_python


}
catch
{
    Write-Output $_
}
finally
{
    Set-Location "$cwd"
}