$content = Get-Content -LiteralPath "G:\SDA\fihirana\baibolyMG_v2.html" -Raw
Write-Host "File length: $($content.Length)"

# Check for external URLs
$httpCount = [regex]::Matches($content, 'https?://').Count
Write-Host "http(s):// occurrences: $httpCount"

# Show each unique URL
$urls = [regex]::Matches($content, 'https?://[^""''<>`n`r ]+') | ForEach-Object { $_.Value } | Sort-Object -Unique
foreach ($u in $urls) {
    Write-Host "  URL: $u"
}
