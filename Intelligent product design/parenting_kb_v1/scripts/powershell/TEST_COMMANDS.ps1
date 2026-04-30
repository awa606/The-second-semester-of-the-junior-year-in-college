param(
    [string]$ApiUrl = "http://127.0.0.1:8000/api/ask"
)

chcp 65001 | Out-Null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding

$tests = @(
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + "6" + [char]0x4E2A + [char]0x6708 + [char]0x7B2C + [char]0x4E00 + [char]0x53E3 + [char]0x8F85 + [char]0x98DF + [char]0x5403 + [char]0x4EC0 + [char]0x4E48 + [char]0xFF1F); age_months = 6 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + [char]0x591A + [char]0x4E45 + [char]0x559D + [char]0x4E00 + [char]0x6B21 + [char]0x5976 + [char]0x7C89); age_months = 3 },
    @{ question = [string]([char]0x5976 + [char]0x7C89 + [char]0x600E + [char]0x4E48 + [char]0x51B2 + [char]0x624D + [char]0x5B89 + [char]0x5168 + [char]0xFF1F); age_months = 2 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + [char]0x7EA2 + [char]0x5C41 + [char]0x5C41 + [char]0x600E + [char]0x4E48 + [char]0x9884 + [char]0x9632 + [char]0xFF1F); age_months = 4 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + [char]0x9F3B + [char]0x585E + [char]0x600E + [char]0x4E48 + [char]0x529E + [char]0xFF1F); age_months = 5 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + [char]0x51E0 + [char]0x4E2A + [char]0x6708 + [char]0x4F1A + [char]0x5750 + [char]0xFF1F); age_months = 7 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + [char]0x62C9 + [char]0x809A + [char]0x5B50 + [char]0x4E00 + [char]0x5929 + [char]0x5F88 + [char]0x591A + [char]0x6B21 + [char]0x600E + [char]0x4E48 + [char]0x529E + [char]0xFF1F); age_months = 8 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + [char]0x6454 + [char]0x5230 + [char]0x5934 + [char]0x600E + [char]0x4E48 + [char]0x529E + [char]0xFF1F); age_months = 10 },
    @{ question = [string]([char]0x5B9D + [char]0x5B9D + "39.5" + [char]0x5EA6 + [char]0x5E03 + [char]0x6D1B + [char]0x82AC + [char]0x5403 + [char]0x51E0 + [char]0x6BEB + [char]0x5347 + [char]0xFF1F); age_months = 8 }
)

foreach ($test in $tests) {
    Write-Host "========================================"
    Write-Host "Question: $($test.question)"

    $body = @{
        question = $test.question
        age_months = $test.age_months
        context = @{}
    } | ConvertTo-Json -Depth 5

    $response = Invoke-RestMethod `
        -Uri $ApiUrl `
        -Method Post `
        -ContentType "application/json; charset=utf-8" `
        -Body $body

    $response | ConvertTo-Json -Depth 10
}
