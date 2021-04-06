# A powershell script that deletes old users in TeamViewer

$token = token
$bearer = "Bearer",$token

$header = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$header.Add("authorization", $bearer)

$devices = (Invoke-RestMethod -Uri "https://webapi.teamviewer.com/api/v1/devices" -Method Get -Headers $header).devices

$90Days = ((Get-Date).AddDays(-90)).GetDateTimeFormats()[5]

ForEach($device in $devices)
{

    if ($device.online_state -eq "Offline")
    {

    $ID = $device.device_id

    $Lastseen = $device.last_seen

            if ($Lastseen -ne $null)
            {

            $LastSeen = ($device.last_seen).Split("T")[0]
            [datetime]$DateLastSeen = $LastSeen

                    if ($DateLastSeen -le $90Days)
                    {

                    Invoke-WebRequest -Uri "Https://webapi.teamviewer.com/api/v1/devices/$ID" -Method Delete -Headers $header
                    Write-Host "Deleted device:"$device.alias -ForegroundColor Yellow
                    
                    }$Lastseen = $null
            }
    }
}