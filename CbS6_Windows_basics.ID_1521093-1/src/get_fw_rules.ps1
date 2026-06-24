$ruleNames = @(
    "Block_http_conn",
    "Allow_rdp_conn",
    "Block_ftp_conn",
    "Block_ping_conn"
)

$outputFile = "$PSScriptRoot\result.txt"

foreach ($name in $ruleNames) {
    $rule = Get-NetFirewallRule -DisplayName $name
    if ($rule) {
        $port = Get-NetFirewallPortFilter -AssociatedNetFirewallRule $rule

        [PSCustomObject]@{
            RuleName      = $rule.DisplayName
            Enabled       = $rule.Enabled
            Direction     = $rule.Direction
            Action        = $rule.Action
            Profile       = $rule.Profile
            Protocol      = $port.Protocol
            LocalPort     = $port.LocalPort
            RemotePort    = $port.RemotePort
        } | Format-Table -AutoSize | Out-File $outputFile -Append

        "`n" | Out-File $outputFile -Append
    }
}
