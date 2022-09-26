const path = require('path');
const express = require('express');
const dotenv = require('dotenv');
const exphbs = require('express-handlebars');
const { resolveSoa } = require('dns');

dotenv.config({ path: './.env'});

const app = express();

// const { } = require('./helpers/hbs');
// const { appendFile } = require('fs');

app.engine('.hbs', exphbs.engine({
    //helpers: {},
    defaultLayout: 'main',
    extname: '.hbs' }))

app.set('view engine', '.hbs');

app.use(express.static(path.join(__dirname, 'public',)))

//ROUTES
app.use('/', require('./routes/index'));

const PORT = process.env.PORT || 3000;

app.listen(
    PORT, console.log(`SERVER running in MODE: ${process.env.NODE_ENV} on PORT: ${PORT}`)
)