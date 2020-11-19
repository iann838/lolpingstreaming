Set oShell = CreateObject("Wscript.Shell")
Dim strArgs
strArgs = "C:\LoLPingStreaming\startup.bat"
oShell.Run strArgs, 0, false
