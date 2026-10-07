<#
.SYNOPSIS
  Import a UTF-8 .sql file into a Postgres container without mangling Unicode.

.DESCRIPTION
  Do NOT use:  Get-Content file.sql | docker exec -i <db> psql ...
  Windows PowerShell 5.1 reads a BOM-less UTF-8 file as Windows-1252 and pipes
  it to native programs as US-ASCII, so every non-ASCII byte becomes "?".
  That is how the desktop bank lost × ÷ − √ ² ≤ ≥ ₱ and curly quotes ("??").

  This script copies the file byte-for-byte into the container (docker cp) and
  runs psql -f inside it with a UTF-8 client encoding, so PowerShell never
  re-encodes the text.

.EXAMPLE
  .\scripts\import-sql-utf8.ps1 -SqlFile .\scripts\seeds\replace_first_20.sql `
      -Container my-postgres -Database civio -User civio
#>
param(
    [Parameter(Mandatory = $true)][string]$SqlFile,
    [Parameter(Mandatory = $true)][string]$Container,
    [Parameter(Mandatory = $true)][string]$Database,
    [Parameter(Mandatory = $true)][string]$User
)

$ErrorActionPreference = 'Stop'
$resolved = (Resolve-Path $SqlFile).Path
$target = "/tmp/" + [IO.Path]::GetFileName($resolved)

docker cp $resolved "${Container}:$target"
try {
    docker exec -e PGCLIENTENCODING=UTF8 $Container `
        psql -v ON_ERROR_STOP=1 -U $User -d $Database -f $target
    if ($LASTEXITCODE -ne 0) { throw "psql exited with $LASTEXITCODE" }
}
finally {
    docker exec $Container rm -f $target | Out-Null
}
