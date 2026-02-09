$mysqlPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$sqlFile = "C:\implantacion\fastapi_plantillascomunes\sql\add_edit_and_votes.sql"
$password = Read-Host "Ingresa la contraseña de MySQL" -AsSecureString
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($password))

& $mysqlPath -u root -p"$plainPassword" -e "USE thomas; source '$sqlFile'"
