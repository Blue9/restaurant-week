const http = require('http')
const fs = require('fs')
const url = require('url')

const server = http.createServer((req, res) => {
  const path = url.parse(req.url).pathname

  switch (path) {
    case '/':
      fs.readFile('./index.html', (err, data) => {
        if (err) {
          res.writeHead(500)
          res.end(`Error: ${err.message}`)
        } else {
          res.writeHead(200, { 'Content-Type': 'text/html' })
          res.end(data)
        }
      })
      break

    case '/data.json':
      fs.readFile('./restaurants-clean.json', (err, data) => {
        if (err) {
          res.writeHead(500)
          res.end(`Error: ${err.message}`)
        } else {
          res.writeHead(200, { 'Content-Type': 'application/json' })
          res.end(data)
        }
      })
      break

    case '/bread.png':
    case '/burger.png':
    case '/chef.png':
    case '/kebab.png':
    case '/latin.png':
    case '/asian.png':
    case '/pizza.png':
      fs.readFile(`./icons${path}`, (err, data) => {
        if (err) {
          res.writeHead(500)
          res.end(`Error: ${err.message}`)
        } else {
          res.writeHead(200, { 'Content-Type': 'image/png' })
          res.end(data)
        }
      })
      break

    default:
      res.writeHead(404)
      res.end('Error: Page not found')
      break
  }
})

server.listen(3000, () => {
  console.log('Server running on http://localhost:3000')
})
