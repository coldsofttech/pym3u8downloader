const express = require('express');
const https = require('https');
const fs = require('fs');
const path = require('path');

const app = express();
const portHttp = 8000;
const portHttps = 8001;

app.use('/files', express.static(path.join(__dirname, 'files')));

app.get('/', (req, res) => {
    const domain = req.hostname || 'localhost';
    const port = req.app.get('port') || (req.connection.encrypted ? portHttps : portHttp);
    res.json({
        domain: domain,
        port: port
    });
});

app.set('port', portHttp);
const httpServer = app.listen(portHttp, () => {
    console.log(`HTTP server running on port ${portHttp}`);
});

const httpsOptions = {
    key: fs.readFileSync(path.join(__dirname, 'key.pem')),
    cert: fs.readFileSync(path.join(__dirname, 'cert.pem'))
};
app.set('port', portHttps);
const httpsServer = https.createServer(httpsOptions, app).listen(portHttps, () => {
    console.log(`HTTPS server running on port ${[portHttps]}`);
});
