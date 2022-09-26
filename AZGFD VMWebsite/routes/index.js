const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.render('landing', {
        layout: 'main'
    })
})

router.get('/logs', (req, res) => {
    res.render('logs', {
        layout: 'main'
    })
})

router.get('/errors', (req, res) => {
    res.render('errors', {
        layout: 'main'
    })
})

module.exports = router;