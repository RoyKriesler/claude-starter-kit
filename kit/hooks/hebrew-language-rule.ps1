$inputJson = [Console]::In.ReadToEnd()
try {
    $data = $inputJson | ConvertFrom-Json
    $prompt = $data.prompt
} catch {
    $prompt = $inputJson
}

if ($prompt -match '\p{IsHebrew}') {
    Write-Output "HEBREW DETECTED. Strict rules:"
    Write-Output "1. No Latin chars inside Hebrew sentences. Tech tokens like SQL, API, parquet, file paths go in code blocks on their own line."
    Write-Output "2. No parens, brackets, curly braces, slashes, pipes, angle brackets inside Hebrew prose. Use comma, em-dash, or newline instead. No Markdown tables containing Hebrew: use numbered sections with bold labels."
    Write-Output "3. Backticks around English do NOT make it safe inside Hebrew sentences."
    Write-Output "4. Hebrew stays clean natural prose, terse."
    Write-Output "5. Self-check every Hebrew sentence before sending."
}
