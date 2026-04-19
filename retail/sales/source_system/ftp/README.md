# Source FTP Server

Local FTP endpoint for source-system file landing.

```powershell
docker compose up -d
```

Connection defaults:

- Host: `localhost`
- Port: `2121`
- User: `source_user`
- Password: `source_pass`

The FTP root maps to the sibling `generated` folder.
