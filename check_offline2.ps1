$content = Get-Content -LiteralPath "G:\SDA\fihirana\baibolyMG_v2.html" -Raw
$urls = [regex]::Matches($content, 'https?://[^\x22\x27\x3e\x3c\x60\n\r ]+') | ForEach-Object { $_.Value } | Sort-Object -Unique
foreach ($u in $urls) {
    Write-Host "  URL: $u"
}
Write-Host "Total unique URLs: $($urls.Count)"
