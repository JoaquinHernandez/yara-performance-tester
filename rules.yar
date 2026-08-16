rule WebShell_PHP_Generic {
    meta:
        description = "Detects common PHP webshell execution patterns"
        author = "BlueTeam"
        severity = "HIGH"
    strings:
        $p1 = "passthru(" ascii nocase
        $p2 = "shell_exec(" ascii nocase
        $p3 = "system(" ascii nocase
        $p4 = "eval(base64_decode(" ascii nocase
    condition:
        any of ($p*)
}

rule Suspicious_High_Cost_Regex {
    meta:
        description = "Simulates an unoptimized rule prone to catastrophic backtracking"
        author = "BlueTeam"
        severity = "LOW"
    strings:
        // Demonstrates regex overhead
        $re = /([a-zA-Z0-9]+)*=([a-zA-Z0-9]+)/
    condition:
        $re
}
