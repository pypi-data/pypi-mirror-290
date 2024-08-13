#!/usr/local/bin/pwsh

param(
    [String] $version = "invalid_version",
    [Switch] $test = $false,
    [Switch] $deploy = $false
)

$cwd = $( Get-Location )
$root = "$PSScriptRoot"

function Test
{
    docker build -t keystone-database -f "$root/tests.Dockerfile" "$root/keystone-database"
    docker run --rm keystone-database
    docker image rm keystone-database
}

try
{
    Set-Location "$root"

    if ($test)
    {
        Test
    }

    if ($deploy)
    {
        Test
        $token = $( op read op://private/gitlab-api-token/password )
        $user = "coneill"

        docker build -t keystone_python .
        foreach ($project in "postrgres", "decorators", "security", "excel", "database", "message-broker", "msgraph", "gitlab")
        {
            docker run `
                --rm `
                -it `
                -e "HATCH_INDEX_AUTH=$token" `
                -e "HATCH_INDEX_USER=$user" `
                -e "PROJECT_PATH=/app/keystone-$project" `
                -e "CI_API_V4_URL=https://gitlab.purplejay.net/api/v4" `
                -e "CI_PROJECT_ID=221" `
                -e "version=$version" `
                keystone_python
        }
    }
}
catch
{
    Write-Output $_
}
finally
{
    Set-Location "$cwd"
}