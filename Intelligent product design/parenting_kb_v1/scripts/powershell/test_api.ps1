chcp 65001 | Out-Null
[Console]::InputEncoding  = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding

$tests = @(
    @{ question = "宝宝6个月第一口辅食吃什么？"; age_months = 6 },
    @{ question = "宝宝红屁屁怎么预防？"; age_months = 4 },
    @{ question = "宝宝拉肚子一天很多次怎么办？"; age_months = 8 }
)

foreach ($t in $tests) {
    Write-Host "=============================="
    Write-Host "测试问题: $($t.question)"
    $body = $t | ConvertTo-Json
    $resp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/ask" `
        -Method Post `
        -ContentType "application/json; charset=utf-8" `
        -Body $body
    $resp | ConvertTo-Json -Depth 10
}